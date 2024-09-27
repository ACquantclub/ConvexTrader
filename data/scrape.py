import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the stock symbol and the period
symbol = 'AAPL'  # Example: Apple stock, you can change this to any stock ticker
period = '1y'    # 1 year worth of data

# Fetch historical equity data using yfinance
def get_equity_data(symbol, period='1y'):
    stock = yf.Ticker(symbol)
    history = stock.history(period=period)
    return history

# Fetch option chain data using yfinance
def get_derivative_data(symbol):
    stock = yf.Ticker(symbol)
    expiration_dates = stock.options
    
    # Collect options data for all expiration dates
    options_data = []
    for exp_date in expiration_dates:
        options = stock.option_chain(exp_date)
        calls = options.calls.assign(Expiration=exp_date, Type='Call')
        puts = options.puts.assign(Expiration=exp_date, Type='Put')
        options_data.append(pd.concat([calls, puts], ignore_index=True))
    
    return pd.concat(options_data, ignore_index=True)

# Save data to CSV
def save_to_csv(data, filename):
    data.to_csv(filename, index=True)
    print(f"Data saved to {filename}")

# Main function to get the data and save to CSV
def main():
    print(f"Fetching 1 year of equity data for {symbol}...")
    equity_data = get_equity_data(symbol)
    save_to_csv(equity_data, f"{symbol}_equity_data.csv")
    
    print(f"Fetching derivative data for {symbol}...")
    derivative_data = get_derivative_data(symbol)
    save_to_csv(derivative_data, f"{symbol}_derivative_data.csv")

    print("Data scraping completed.")

if __name__ == "__main__":
    main()