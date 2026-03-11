import pandas as pd
import yfinance as yf
from datetime import datetime
import os

# -----------------------------
# 1️⃣ Load portfolio holdings
# -----------------------------
portfolio_file = "portfolio.csv"  # CSV with columns: Ticker,Shares,AvgCost
portfolio = pd.read_csv(portfolio_file)
tickers = portfolio["Ticker"].tolist()

# -----------------------------
# 2️⃣ Fetch latest stock prices
# -----------------------------
data = yf.download(tickers, period="1d")["Close"]
latest_prices = data.iloc[-1]

# -----------------------------
# 3️⃣ Prepare price history entry
# -----------------------------
now = datetime.utcnow()
prices = pd.DataFrame({
    "datetime": [now] * len(latest_prices),
    "ticker": latest_prices.index,
    "price": latest_prices.values
})

prices_file = "prices_history.csv"
if os.path.exists(prices_file):
    # Append to existing file without headers
    prices.to_csv(prices_file, mode="a", header=False, index=False)
else:
    # File doesn't exist → write headers
    prices.to_csv(prices_file, index=False)

# -----------------------------
# 4️⃣ Update portfolio value
# -----------------------------
portfolio["price"] = portfolio["Ticker"].map(latest_prices)
portfolio["value"] = portfolio["Shares"] * portfolio["price"]
total_value = portfolio["value"].sum()

value_row = pd.DataFrame({
    "datetime": [now],
    "portfolio_value": [total_value]
})

value_file = "portfolio_value_history.csv"
if os.path.exists(value_file):
    value_row.to_csv(value_file, mode="a", header=False, index=False)
else:
    value_row.to_csv(value_file, index=False)

# -----------------------------
# ✅ Finished
# -----------------------------
