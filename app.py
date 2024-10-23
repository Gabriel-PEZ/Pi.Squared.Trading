import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch stock data and handle errors
def fetch_stock_data(tickers, start_date):
    stock_data = {}
    invalid_tickers = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date)['Close']
            if hist.empty:
                invalid_tickers.append(ticker)
            else:
                stock_data[ticker] = hist
        except Exception:
            invalid_tickers.append(ticker)
    return pd.DataFrame(stock_data), invalid_tickers

# Function to calculate portfolio performance in percentages from day 1
def calculate_portfolio_performance(data, weights):
    # Normalize the stock data by dividing by the first value
    normalized_data = data / data.iloc[0] * 100
    # Multiply by weights to get portfolio value over time
    portfolio_performance = (normalized_data * weights).sum(axis=1)
    return portfolio_performance

# Streamlit UI
st.title("Portfolio Performance Viewer")

# Step 1: Input stock tickers (any stock, not predefined)
st.sidebar.header("Portfolio Configuration")
st.sidebar.write("Add stock tickers and weights below (e.g., AAPL, MSFT, GOOGL, etc.)")

tickers = []
weights = []

# Allow the user to input multiple tickers and corresponding weights
num_stocks = st.sidebar.number_input("How many stocks do you want in your portfolio?", min_value=1, max_value=20, value=3)

for i in range(num_stocks):
    ticker = st.sidebar.text_input(f"Stock {i+1} ticker:", value="", key=f"ticker_{i}")
    tickers.append(ticker.upper())

    # Step 2: Enter weights for each stock as a numerical input (no slider)
    weight = st.sidebar.number_input(f"Weight for {ticker} (as a fraction, e.g., 0.5 for 50%):", min_value=0.0, max_value=1.0, value=0.2, key=f"weight_{i}")
    weights.append(weight)

# Ensure weights sum to 1
total_weight = sum(weights)

# Step 3: Select start date for investing (default 01/01/2024)
start_date = st.sidebar.date_input("Start date:", pd.to_datetime("2024-01-01"))

# Step 4: Display the portfolio table
st.subheader("Portfolio Overview")
portfolio_data = pd.DataFrame({
    "Stock": tickers,
    "Weight": weights
})
st.table(portfolio_data)

# Proceed only if the weights sum to 1.0
if total_weight != 1.0:
    st.sidebar.error(f"Error: Weights must sum up to 1. Current sum: {total_weight:.2f}")
else:
    # Fetch stock data for selected stocks and handle invalid tickers
    stock_data, invalid_tickers = fetch_stock_data(tickers, start_date)

    if invalid_tickers:
        st.error(f"Invalid tickers: {', '.join(invalid_tickers)}. Please check the stock symbols.")
    elif not stock_data.empty:
        # Step 5: Calculate portfolio performance in percentage
        portfolio_performance = calculate_portfolio_performance(stock_data, weights)

        # Step 6: Plot portfolio performance
        st.subheader("Portfolio Performance (in %)")
        plt.figure(figsize=(10, 6))
        plt.plot(portfolio_performance.index, portfolio_performance, label="Portfolio Performance", color="blue")
        plt.title("Portfolio Performance Over Time")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value (%)")
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.error("No data found for the selected tickers or start date.")