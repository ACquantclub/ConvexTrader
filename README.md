# Applications-of-Convex-Optimization

[![Pytest + CI/CD](https://github.com/ACquantclub/ConvexTrader/actions/workflows/github-actions-tests.yml/badge.svg)](https://github.com/ACquantclub/ConvexTrader/actions/workflows/github-actions-tests.yml)
[![Coverage Status](https://coveralls.io/github/ACquantclub/ConvexTrader/badge.svg)](https://coveralls.io/github/ACquantclub/ConvexTrader)
[![Docs Build Deployment](https://github.com/liamjdavis/Sudoku-SMT-Solvers/actions/workflows/docs.yml/badge.svg)](https://github.com/ACQuantClub/ConvexTrader/actions/workflows/docs.yml)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://acquantclub.com/ConvexTrader)

## About

This repository contains a Python package, ConvexTrader, for applications of convex application methods to portfolio optimization. Created by members of the Amherst College Quant Club as part of the 2024-2025 school year, this package is based upon a paper by Dhyey Mavani '25, which can be found [here](https://github.com/ACquantclub/ConvexTrader/blob/main/refs/Optimization_Final_Report_Dhyey_Mavani.pdf).

## Installation & Use

### Installation
To run the code locally, you can install with `pip`

```bash
pip install ConvexTrader
```

### Using Optimization Techniques

```python
from ConvexTrader import Portfolio
from ConvexTrader import Trade, TradeType
from ConvexTrader.single_period_optimization import single_period_optimization
from ConvexTrader.portfolio_exceptions import ValidationError, OptimizationError

# Example Portfolio
portfolio = Portfolio()
trades = [
    Trade("AAPL", 100, 150.0, datetime(2023, 1, 1), TradeType.BUY),
    Trade("GOOGL", 50, 2000.0, datetime(2023, 1, 2), TradeType.BUY),
    Trade("MSFT", 75, 300.0, datetime(2023, 1, 3), TradeType.BUY),
]
for trade in trades:
    portfolio.execute_trade(trade)

# Example Trade (single period)

r_t = np.array([0.05, 0.07, 0.02])
w_t = sample_portfolio.weights_vector
gamma = 1.0

def phi_trade(z):
    return cp.sum(cp.abs(z))

def phi_hold(w):
    return cp.sum(cp.square(w))

# this returns the optimal trade vector to be used
result = single_period_optimization(r_t, w_t, gamma, phi_trade, phi_hold)

```

### Running Tests

To run the test suite, use
```bash
pytest
```

## Contributing

We welcome contributions in the form of coding new applications of convex optimization towards trading, or anything to help improve the tool. Here's how you can help:

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

### Installing Dependencies and Hooks

1. **Install the required dependencies from the `requirements.txt` file**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Set Up Pre-Commit Hooks**:  
   Install and configure pre-commit hooks to maintain code quality:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

   To manually run the hooks and verify code compliance, use:
   ```bash
   pre-commit run
   ```

### Adding Tests and Changes

1. **Testing and Coverage Requirements**:  
   - Write tests for any new code or modifications.
   - Use `pytest` for running tests:
     ```bash
     pytest
     ```
   - Ensure the test coverage is at least 90%
  
2. **Add and Commit Your Changes**:  
   - Follow the existing code style and structure.
   - Verify that all pre-commit hooks pass and the test coverage meets the minimum requirement.
   ```bash
   git add .
   pre-commit run
   git commit -m "Description of your changes"
   ```

3. **Push Your Branch**:
   Push your changes to your forked repository:
   ```bash
   git push --setup-upstream origin
   ```

4. **Open a PR for us to review**

Thank you for your interest in contributing to ConvexTrader! Your efforts help make this project better for everyone.

## Contact

For any questions about the package, please reach out to trading at amherst.edu
