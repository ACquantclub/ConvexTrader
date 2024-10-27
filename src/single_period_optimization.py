mport numpy as np
import cvxpy as cp

def single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold):
    # Number of assets
    n = len(r_t)

    # Decision variable: trade vector z_t
    z_t = cp.Variable(n)

    # Transaction and holding cost
    trade_cost = phi_trade(z_t)
    hold_cost = phi_hold(w_t + z_t)

    # Define the risk measure: Assume a simple quadratic risk model
    sigma_t = np.eye(n)  # Placeholder for the covariance matrix (to be replaced with real data)
    risk = cp.quad_form(w_t + z_t, sigma_t)

    # Objective function: maximize return minus risk and costs
    objective = cp.Maximize(r_t.T @ z_t - gamma * risk - trade_cost - hold_cost)

    # Constraints: Self-financing without explicitly setting trade_cost and hold_cost to zero
    # Allow the portfolio weights to sum up to 1 after trades (budget constraint)
    constraints = [cp.sum(w_t + z_t) == 1] 

    # Problem definition
    problem = cp.Problem(objective, constraints)

    # Solve the problem if the problem adheres to DCP rules
    if(problem.is_dcp()):
        problem.solve()
        return z_t.value
    else:
        print("Error: problem with inputted values was not DCP")
        return -1