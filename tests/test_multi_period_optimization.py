import pytest
import os
import sys
import numpy as np
from datetime import datetime

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from Portfolio import Portfolio
from Trade import Trade, TradeType
from multi_period_optimization import multi_period_optimization


def test_multi_period_optimization_basic():
    H = 3  # Horizon
    portfolio_size = 2  # Two assets

    # Corrected mock inputs
    r_t = np.array([[0.05, 0.02], [0.04, 0.03], [0.06, 0.01]])  # Expected returns (3 rows)
    gamma_t = np.array([0.5, 0.4, 0.3])  # Risk aversion parameters (3 elements)
    psi_t = np.array([[0.1, 0.2], [0.15, 0.25], [0.1, 0.15]])  # Risk factors (3 rows)
    phi_trade = [np.array([0.02, 0.03]), np.array([0.01, 0.04]), np.array([0.03, 0.02])]
    phi_hold = [np.array([0.01, 0.01]), np.array([0.01, 0.01]), np.array([0.01, 0.01])]

    class MockPortfolio:
        def __init__(self):
            self.weights_vector = np.array([0.6, 0.4])  # Two assets

    mock_portfolio = MockPortfolio()

    z = multi_period_optimization(H, r_t, mock_portfolio, gamma_t, psi_t, phi_trade, phi_hold)

    assert z is not None
    assert z.shape == (portfolio_size, H - 1)


def test_multi_period_optimize_basic():
    H = 3
    portfolio = Portfolio()

    trade_date = datetime.now()
    portfolio.execute_trade(Trade("AAPL", 10, TradeType.BUY, trade_date, TradeType.BUY))
    portfolio.execute_trade(Trade("GOOGL", 20, TradeType.BUY, trade_date, TradeType.BUY))

    r_t = np.array([[0.05, 0.02], [0.04, 0.03], [0.06, 0.01]])
    gamma_t = np.array([0.5, 0.4, 0.3])
    psi_t = np.array([[0.1, 0.2], [0.15, 0.25], [0.1, 0.15]])
    phi_trade = [np.array([0.02, 0.03]), np.array([0.01, 0.04]), np.array([0.03, 0.02])]
    phi_hold = [np.array([0.01, 0.01]), np.array([0.01, 0.01]), np.array([0.01, 0.01])]

    z = portfolio.multi_period_optimize(H, r_t, gamma_t, psi_t, phi_trade, phi_hold)

    assert z is not None
    assert z.shape == (len(portfolio.symbols), H - 1)


def test_multi_period_optimize_invalid_inputs():
    H = 3  # Horizon
    portfolio = Portfolio()

    # Mock initial trades to populate portfolio
    trade_date = datetime.now()
    portfolio.execute_trade(Trade("AAPL", 10, TradeType.BUY, trade_date, TradeType.BUY))
    portfolio.execute_trade(Trade("GOOGL", 20, TradeType.BUY, trade_date, TradeType.BUY))

    # Provide fewer rows in `r_t` than `H`
    r_t = np.array([[0.05, 0.02], [0.04, 0.03]])  # Only 2 rows instead of 3
    gamma_t = np.array([0.5, 0.4, 0.3])  # Correct length
    psi_t = np.array([[0.1, 0.2], [0.15, 0.25], [0.1, 0.15]])  # Correct dimensions
    phi_trade = [np.array([0.02, 0.03]), np.array([0.01, 0.04]), np.array([0.03, 0.02])]
    phi_hold = [np.array([0.01, 0.01]), np.array([0.01, 0.01]), np.array([0.01, 0.01])]

    # Expect error for mismatched dimensions
    with pytest.raises(IndexError):
        portfolio.multi_period_optimize(H, r_t, gamma_t, psi_t, phi_trade, phi_hold)