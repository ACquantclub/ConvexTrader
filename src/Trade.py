from enum import Enum, auto
from datetime import datetime

class TradeType(Enum):
    """
    Enum representing the type of trade, either a BUY or SELL.
    """
    BUY = auto()
    SELL = auto()

class Trade:
    def __init__(self, symbol: str, quantity: int, price: float, trade_date: datetime, trade_type: TradeType):
        """
        Represents a trade in a financial portfolio, either a buy or sell order.
        - symbol: The ticker symbol of the stock being traded (e.g., 'AAPL', 'GOOGL').
        - quantity: The number of shares being bought or sold.
        - price: The price per share at which the trade was executed.
        - trade_date: The date and time the trade took place.
        - trade_type: An instance of TradeType enum indicating if it's a BUY or SELL trade.
        """
        self.symbol = symbol
        self.quantity = quantity
        self.price = price 
        self.trade_date = trade_date 
        
        # Ensure that trade_type is a valid instance of the TradeType enum
        if not isinstance(trade_type, TradeType):
            raise ValueError("trade_type must be a TradeType enum")
        self.trade_type = trade_type 

    def __repr__(self):
        """
        String representation of the Trade object, showing essential trade details for easier readability.
        """
        return (f"<Trade(symbol={self.symbol}, quantity={self.quantity}, price={self.price}, "
                f"date={self.trade_date.strftime('%Y-%m-%d %H:%M:%S')}, type={self.trade_type.name})>")
