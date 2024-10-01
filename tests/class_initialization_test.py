import sys
import os
import pytest
import numpy as np
from datetime import datetime

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from Portfolio import Portfolio
from Trade import Trade, TradeType

# Fixture to create a sample portfolio with some trades
@pytest.fixture
def sample_portfolio():
    portfolio = Portfolio()
    trades = [
        Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), TradeType.BUY),
        Trade("GOOGL", 50, 2000.0, datetime(2023, 1, 2), TradeType.BUY),
        Trade("MSFT", 75, 300.0, datetime(2023, 1, 3), TradeType.BUY)
    ]
    for trade in trades:
        portfolio.execute_trade(trade)
    return portfolio

# Test to verify trade creation
def test_trade_creation():
    trade = Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), TradeType.BUY)
    assert trade.symbol == "AAPL"
    assert trade.quantity == 100
    assert trade.price == 150.0
    assert trade.trade_date == datetime(2023, 1, 1)
    assert trade.trade_type == TradeType.BUY

# Test to verify invalid trade type raises ValueError
def test_trade_invalid_type():
    with pytest.raises(ValueError):
        Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), "INVALID")

# Test to verify portfolio creation
def test_portfolio_creation():
    portfolio = Portfolio()
    assert len(portfolio.holdings) == 0
    assert len(portfolio.trades) == 0
    assert len(portfolio.symbols) == 0
    assert len(portfolio.holdings_vector) == 0
    assert len(portfolio.weights_vector) == 0

# Test to verify executing trades updates the portfolio correctly
def test_execute_trade(sample_portfolio):
    assert len(sample_portfolio.holdings) == 3
    assert len(sample_portfolio.trades) == 3
    assert len(sample_portfolio.symbols) == 3
    assert len(sample_portfolio.holdings_vector) == 3
    assert len(sample_portfolio.weights_vector) == 3

# Test to verify holdings vector is updated correctly
def test_holdings_vector(sample_portfolio):
    np.testing.assert_array_equal(sample_portfolio.holdings_vector, np.array([100, 50, 75]))

# Test to verify weights vector is calculated correctly
def test_weights_vector(sample_portfolio):
    expected_weights = np.array([100, 50, 75]) / 225
    np.testing.assert_array_almost_equal(sample_portfolio.weights_vector, expected_weights)

# Test to verify get_weights method returns correct weights
def test_get_weights(sample_portfolio):
    weights = sample_portfolio.get_weights()
    assert len(weights) == 3
    assert weights["AAPL"] == pytest.approx(100/225)
    assert weights["GOOGL"] == pytest.approx(50/225)
    assert weights["MSFT"] == pytest.approx(75/225)

# Test to verify total value calculation
def test_total_value(sample_portfolio):
    current_prices = {"AAPL": 160.0, "GOOGL": 2100.0, "MSFT": 310.0}
    total_value = sample_portfolio.total_value(current_prices)
    expected_value = 100 * 160.0 + 50 * 2100.0 + 75 * 310.0
    assert total_value == pytest.approx(expected_value)

# Test to verify selling a trade updates the portfolio correctly
def test_sell_trade(sample_portfolio):
    sell_trade = Trade("AAPL", 50, 160.0, datetime(2023, 1, 4), TradeType.SELL)
    sample_portfolio.execute_trade(sell_trade)
    assert sample_portfolio.holdings["AAPL"] == 50
    np.testing.assert_array_equal(sample_portfolio.holdings_vector, np.array([50, 50, 75]))

# Test to verify selling more than available raises ValueError
def test_sell_too_much(sample_portfolio):
    sell_trade = Trade("AAPL", 150, 160.0, datetime(2023, 1, 4), TradeType.SELL)
    with pytest.raises(ValueError):
        sample_portfolio.execute_trade(sell_trade)

# Test to verify selling all shares removes the symbol from holdings
def test_sell_all(sample_portfolio):
    sell_trade = Trade("AAPL", 100, 160.0, datetime(2023, 1, 4), TradeType.SELL)
    sample_portfolio.execute_trade(sell_trade)
    assert "AAPL" not in sample_portfolio.holdings
    np.testing.assert_array_equal(sample_portfolio.holdings_vector, np.array([0, 50, 75]))

# Run the tests
if __name__ == "__main__":
    pytest.main()
