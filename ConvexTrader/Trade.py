from enum import Enum, auto
from datetime import datetime
from portfolio_exceptions import ValidationError


class TradeType(Enum):
    """
    Enum representing the type of trade, either a BUY or SELL.
    """

    BUY = auto()
    SELL = auto()


class Trade:
    def __init__(
        self,
        symbol: str,
        quantity: int,
        price: float,
        trade_date: datetime,
        trade_type: TradeType,
    ):
        """
        Represents a trade in a financial portfolio.

        Args:
            symbol: The ticker symbol of the stock being traded (e.g., 'AAPL', 'GOOGL')
            quantity: The number of shares being bought or sold
            price: The price per share at which the trade was executed
            trade_date: The date and time the trade took place
            trade_type: An instance of TradeType enum indicating if it's a BUY or SELL trade

        Raises:
            ValidationError: If any input parameters are invalid
        """
        if not isinstance(symbol, str) or not symbol:
            raise ValidationError(
                "Invalid symbol",
                details=f"Symbol must be non-empty string, got {type(symbol)}",
            )

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValidationError(
                "Invalid quantity",
                details=f"Quantity must be positive integer, got {quantity}",
            )

        if not isinstance(price, (int, float)) or price <= 0:
            raise ValidationError(
                "Invalid price", details=f"Price must be positive number, got {price}"
            )

        if not isinstance(trade_date, datetime):
            raise ValidationError(
                "Invalid trade date",
                details=f"Expected datetime object, got {type(trade_date)}",
            )

        if not isinstance(trade_type, TradeType):
            raise ValidationError(
                "Invalid trade type",
                details=f"Expected TradeType enum, got {type(trade_type)}",
            )

        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.trade_date = trade_date
        self.trade_type = trade_type

    def __repr__(self):
        """String representation of the Trade object."""
        return (
            f"<Trade(symbol={self.symbol}, quantity={self.quantity}, price={self.price}, "
            f"date={self.trade_date.strftime('%Y-%m-%d %H:%M:%S')}, type={self.trade_type.name})>"
        )
