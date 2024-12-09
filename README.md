# Applications-of-Convex-Optimization

Fall 2024 Project: Applications of Convex Optimization

## Installation

### Setting Up a Virtual Environment

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Applications-of-Convex-Optimization.git
    cd Applications-of-Convex-Optimization
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv env
    ```

3. **Activate the virtual environment**:
    - On macOS and Linux:
        ```bash
        source env/bin/activate
        ```
    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```

### Installing Dependencies

1. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

### Running Tests

1. **Navigate to the tests directory**:
    ```bash
    cd tests
    ```

2. Follow the instructions in the README located in the tests directory to run the tests.


## Examples

### Quick Start Example
```bash
from datetime import datetime
from ConvexTrader import Portfolio, Trade, TradeType

# initialize a sample portfolio
portfolio = Portfolio()

# initialize sample trades to perform trades in portfolio
trades = [
    Trade("V", 100, 300.0, datetime(2024, 1, 1), TradeType.BUY),
    Trade("AXP", 50, 350.0, datetime(2024, 1, 2), TradeType.BUY),
    Trade("MA", 50, 550.0, datetime(2024, 1, 3), TradeType.BUY),
]

# execute trades
for trade in trades:
    portfolio.execute_trade(trade)
print(portfolio.holdings)
```
