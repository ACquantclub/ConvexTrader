import numpy as np
import cvxpy as cp

def multi_period_optimization(H, r_t, portfolio, gamma_t, psi_t, phi_trade, phi_hold):
    n_assets = len(portfolio.weights_vector)

    # Trades normalized by total portfolio value
    z = cp.Variable((n_assets, H - 1))

    constraints = []
    objective_terms = []

    # Portfolio weights at period tau - 1
    prev_w = portfolio.weights_vector

    for i in range(1, H):
        cur_w = prev_w + z[:, i-1]

        # Objective function for some future period tau (represented by i), where t+1 <= tau <= t + H and t represents the current period
        # r_t[i] is the expected return of each stock for period tau given information at period t
        # cur_w is the portfolio weights at period tau
        # gamma_t[i] is the risk aversion parameter for period tau
        # psi_t[i] is the risk factor of each stock for period tau
        # phi_trade[i] is the transaction cost of each stock for period tau
        # phi_hold[i] is the holding cost of each stock for period tau
        expected_return = cp.matmul(r_t[i], cur_w)
        risk = gamma_t[i] * cp.sum(cp.multiply(psi_t[i], cp.square(cur_w)))
        holding_cost = cp.sum(cp.multiply(phi_hold[i], cur_w))
        transaction_cost = cp.sum(cp.multiply(phi_trade[i], cp.abs(z[:, i-1])))
        
        objective_terms.append(expected_return - risk - holding_cost - transaction_cost)

        # Self-financing constraint
        constraints.append(cp.sum(cur_w) == 1)

        prev_w = cur_w

    # Define the optimization problem
    objective = cp.Maximize(cp.sum(objective_terms))
    problem = cp.Problem(objective, constraints)

    # Solve the problem if the problem adheres to DCP rules
    if problem.is_dcp():
        problem.solve()
        return z.value
    else:
        print("Error: problem with inputted values was not DCP")
        return -1