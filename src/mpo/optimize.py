# Performing multi-period convex optimization to find the optimal portfolio allocation

import numpy as np
import cvxpy as cp

def optimize(H, r_t, portfolio, gamma_t, psi_t, phi_trade, phi_hold):

    # Trades normalized by total portfolio value
    z = cp.Variable((len(portfolio.weights_vector) + 1, H))

    # Output of the objective function for each period tau, where t+1 <= tau <= t + H
    objective_vals = np.empty(H - 1)

    constraints = np.empty(H - 1, dtype=cp.constraints.Inequality)

    # Portfolio weights at period tau - 1
    prev_w = np.array([portfolio.weights_vector + z[:, 0]])

    # Portfolio weights at period tau
    cur_w = None


    for i in range(1, H):
        cur_w = prev_w + z[:, i]

        # Objective function for some future period tau (represented by i), where t+1 <= tau <= t + H and t represents the current period
        # r_t[i] is the expected return of each stock for period tau given information at period t
        # cur_w is the portfolio weights at period tau
        # gamma_t[i] is the risk aversion parameter for period tau
        # psi_t[i] is the risk factor of each stock for period tau
        # phi_trade[i] is the transaction cost of each stock for period tau
        # phi_hold[i] is the holding cost of each stock for period tau
        objective_vals[i-1] = np.dot(r_t[i], cur_w) - gamma_t[i] * psi_t[i] * cur_w - np.dot(phi_hold[i], cur_w) - np.dot(phi_trade[i], cur_w - prev_w)

        # Self financing constraint
        constraints[i-1] = cp.sum(cur_w) == 1

        prev_w = cur_w
            
    objective = cp.Maximize(cp.sum(objective_vals))

    problem = cp.Problem(objective, constraints)

    # Solve the problem if the problem adheres to DCP rules
    if(problem.is_dcp()):
        problem.solve()
        return z.value
    else:
        print("Error: problem with inputted values was not DCP")
        return -1
