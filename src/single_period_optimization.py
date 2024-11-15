import numpy as np
import cvxpy as cp

def single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold):
    # Number of assets
    n = len(r_t)

    # Decision variable: trade vector z_t
    z_t = cp.Variable(n)

    # Transaction and holding cost with scaling
    trade_cost = 0.01 * phi_trade(z_t)
    hold_cost = 0.01 * phi_hold(w_t + z_t)

    # Define the risk measure: Assume a simple quadratic risk model
    sigma_t = np.eye(n)  # Placeholder for the covariance matrix
    risk = gamma * (cp.quad_form(w_t + z_t, sigma_t) / n)

    # Objective function: maximize return minus risk and costs
    objective = cp.Maximize(r_t.T @ z_t - risk - trade_cost - hold_cost)

    # Define all constraints in one place
    constraints = [
        cp.sum(w_t + z_t) == 1,  # Budget constraint
        z_t >= -w_t  # No-shorting constraint: Cannot sell more than we own
    ]

    # Add constraint for minimal trading when expected returns are zero
    if np.allclose(r_t, 0):
        constraints.append(cp.norm(z_t, 1) <= 1e-3)  # Force very small trades

    # Problem definition
    problem = cp.Problem(objective, constraints)

    # Solve the problem if it adheres to DCP rules
    if problem.is_dcp():
        problem.solve()
        return z_t.value if problem.status == cp.OPTIMAL else np.zeros(n)
    else:
        print("Error: problem with inputted values was not DCP")
        return np.zeros(n)