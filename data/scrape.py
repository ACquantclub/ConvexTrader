import yfinance as yf
import pandas as pd

# Define the stock symbols and the period
symbols = ["AAPL", "MSFT", "GOOGL"]  # Example: List of tickers
period = "1y"  # 1 year worth of data


# Fetch historical equity data using yfinance
def get_equity_data(symbols, period="1y"):
    equity_data = []
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        history = stock.history(period=period)
        history["Ticker"] = symbol
        equity_data.append(history)
    return pd.concat(equity_data)


# Fetch option chain data using yfinance
def get_derivative_data(symbols):
    options_data = []
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        expiration_dates = stock.options
        for exp_date in expiration_dates:
            options = stock.option_chain(exp_date)
            calls = options.calls.assign(
                Expiration=exp_date, Type="Call", Ticker=symbol
            )
            puts = options.puts.assign(Expiration=exp_date, Type="Put", Ticker=symbol)
            options_data.append(pd.concat([calls, puts], ignore_index=True))
    return pd.concat(options_data, ignore_index=True)


# Save data to CSV
def save_to_csv(data, filename):
    data.to_csv(filename, index=True)
    print(f"Data saved to {filename}")


# Main function to get the data and save to CSV
def main():
    print("Fetching equity data for all symbols...")
    equity_data = get_equity_data(symbols)
    save_to_csv(equity_data, "consolidated_equity_data.csv")

    print("Fetching derivative data for all symbols...")
    derivative_data = get_derivative_data(symbols)
    save_to_csv(derivative_data, "consolidated_derivative_data.csv")

    print("Data scraping completed.")


if __name__ == "__main__":
    main()
