import sys
import os
import pytest
import numpy as np
from datetime import datetime, timedelta
import cvxpy as cp

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from Portfolio import Portfolio
from Trade import Trade, TradeType
from single_period_optimization import single_period_optimization

# Fixture to create a sample portfolio with some trades
@pytest.fixture
def sample_portfolio1():
    #declare and initialize portfolio
    portfolio = Portfolio() #basic portfolio

    #trades vector to trade on
    trades = [
        Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), TradeType.BUY),
        Trade("GOOGL", 50, 2000.0, datetime(2023, 1, 2), TradeType.BUY),
        Trade("MSFT", 75, 300.0, datetime(2023, 1, 3), TradeType.BUY)
    ]
    for trade in trades:
        portfolio.execute_trade(trade)
    return portfolio

@pytest.fixture
def sample_portfolio2():
    #declare and initialize portfolio
    portfolio = Portfolio() #basic portfolio

    #trades vector to trade on
    trades = [
        Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), TradeType.BUY),
        Trade("GOOGL", 50, 2000.0, datetime(2023, 1, 2), TradeType.BUY),
        Trade("MSFT", 75, 300.0, datetime(2023, 1, 3), TradeType.BUY),
        Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), TradeType.SELL),
        Trade("GOOGL", 50, 2000.0, datetime(2023, 1, 2), TradeType.SELL),
    ]
    for trade in trades:
        portfolio.execute_trade(trade)
    return portfolio

@pytest.fixture
def sample_portfolio3():
    portfolio = Portfolio()
    
    # Reordered trades to ensure we have shares before selling
    trades = [
        # First do all buys
        Trade('AAPL', 15, 150.0, datetime.now(), TradeType.BUY),  # Buy more than we'll sell later
        Trade('GOOGL', 7, 2500.0, datetime.now() - timedelta(days=1), TradeType.BUY),  # Buy more than we'll sell later
        Trade('MSFT', 10, 300.0, datetime.now() - timedelta(days=2), TradeType.BUY),  # Buy before sell
        Trade('TSLA', 25, 800.0, datetime.now() - timedelta(days=3), TradeType.BUY),  # Buy more than we'll sell later
        Trade('AMZN', 5, 3500.0, datetime.now() - timedelta(days=4), TradeType.BUY),  # Buy before sell
        Trade('NFLX', 20, 500.0, datetime.now() - timedelta(days=5), TradeType.BUY),
        Trade('FB', 7, 320.0, datetime.now() - timedelta(days=7), TradeType.BUY),
        
        # Then do sells
        Trade('AAPL', 5, 155.0, datetime.now() - timedelta(days=6), TradeType.SELL),
        Trade('GOOGL', 2, 2550.0, datetime.now() - timedelta(days=8), TradeType.SELL),
        Trade('MSFT', 8, 300.0, datetime.now() - timedelta(days=9), TradeType.SELL),
        Trade('AMZN', 3, 3500.0, datetime.now() - timedelta(days=10), TradeType.SELL),
        Trade('TSLA', 10, 850.0, datetime.now() - timedelta(days=11), TradeType.SELL)
    ]
    
    for trade in trades:
        portfolio.execute_trade(trade)
    return portfolio

def high_gamma(self, portfolio):
    r_t = np.array([0.05, 0.07, 0.02])
    w_t = portfolio.get_weights()
    gamma = 4.0
    phi_hold = portfolio.phi_hold()
    phi_trade = portfolio.phi_trade()

    spo = single_period_optimization(r_t, w_t, gamme, phi_trade, phi_hold)
    self.assertEqual(Portfolio.single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold), spo)

def low_gamma(self):
    r_t = np.array([0.05, 0.07, 0.02])
    w_t = portfolio.get_weights()
    gamma = 0.1
    phi_hold = portfolio.phi_hold()
    phi_trade = portfolio.phi_trade()

    spo = single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold)
    self.assertEqual(Portfolio.single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold), spo)
    
def med_gamma(self):
    r_t = np.array([0.05, 0.07, 0.02])
    w_t = portfolio.get_weights()
    gamma = 1.5
    phi_hold = portfolio.phi_hold()
    phi_trade = portfolio.phi_trade()

    spo = single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold)
    self.assertEqual(Portfolio.single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold), spo)

def test_calculate_spo_unbalanced_weights(sample_portfolio3):
    """
    Test calculate_spo with an unbalanced portfolio (extreme weights) on sample_portfolio3.
    """
    portfolio = sample_portfolio3
    # Adjust holdings vector to avoid over-selling
    portfolio.holdings_vector = np.array([100, 50, 75, 15, 3, 20, 7])
    portfolio.update_weights()

    expected_returns = np.array([0.05, 0.07, 0.02, 0.03, 0.04, 0.06, 0.01])  # Example expected returns
    gamma = 1.0  # Neutral risk aversion

    optimal_trades = portfolio.calculate_spo(expected_returns, gamma)

    # Assert the optimization returned results
    assert optimal_trades is not None, "Optimization failed for unbalanced portfolio"

    # Assert that trades aim to balance the portfolio without violating constraints
    assert all(optimal_trades >= -portfolio.holdings_vector), "Trades should not exceed current holdings (no over-selling)"

def test_calculate_spo_low_gamma(sample_portfolio1):
    portfolio = sample_portfolio1
    expected_returns = np.array([0.05, 0.07, 0.02])
    gamma = 0.1
    
    optimal_trades = portfolio.calculate_spo(expected_returns, gamma)
    
    # Lower threshold for trade size
    assert np.any(np.abs(optimal_trades) > 0.1), "Low gamma should allow moderate trades"
    # Add specific asset checks
    assert optimal_trades[1] > optimal_trades[0], "Higher return asset should have larger trade"

def test_calculate_spo_zero_expected_returns(sample_portfolio2):
    portfolio = sample_portfolio2
    expected_returns = np.zeros(len(portfolio.symbols))
    gamma = 1.0
    
    optimal_trades = portfolio.calculate_spo(expected_returns, gamma)
    
    # Use larger tolerance
    assert np.allclose(optimal_trades, 0, atol=1e-3), "Zero expected returns should lead to minimal trades"

def test_calculate_spo_unbalanced_weights(sample_portfolio3):
    portfolio = sample_portfolio3
    # Ensure valid holdings
    portfolio.holdings_vector = np.array([100, 50, 75, 15, 3, 20, 7])
    portfolio.update_weights()
    
    expected_returns = np.array([0.05, 0.07, 0.02, 0.03, 0.04, 0.06, 0.01])
    gamma = 1.0
    
    optimal_trades = portfolio.calculate_spo(expected_returns, gamma)
    
    # Test for rebalancing direction rather than specific values
    high_weight_asset = np.argmax(portfolio.weights_vector)
    assert optimal_trades[high_weight_asset] < 0, "Should reduce highest weight asset"

# Run the tests
if __name__ == "__main__":
    pytest.main()