import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch stock data
def fetch_stock_data(tickers, start_date):
    stock_data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        stock_data[ticker] = stock.history(start=start_date)['Close']
    return pd.DataFrame(stock_data)

# Function to calculate portfolio performance
def calculate_portfolio_performance(data, weights):
    # Normalize the stock data by dividing by the first value
    normalized_data = data / data.iloc[0]
    # Multiply by weights to get portfolio value over time
    portfolio_performance = (normalized_data * weights).sum(axis=1)
    return portfolio_performance

# Streamlit UI
st.title("Portfolio Performance Viewer")

# Step 1: Select stocks
st.sidebar.header("Portfolio Configuration")
tickers = st.sidebar.multiselect(
    "Select stock tickers:",
    options=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NVDA", "NFLX", "BABA", "V"],
    default=["AAPL", "MSFT", "GOOGL"]
)

# Step 2: Select weights for each stock
if tickers:
    weights = []
    st.sidebar.subheader("Set Weights for Each Stock")
    for ticker in tickers:
        weight = st.sidebar.slider(f"Weight for {ticker}:", 0.0, 1.0, 0.2, 0.01)
        weights.append(weight)

    # Ensure weights sum to 1
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]  # Normalize weights if they don't sum to 1

    # Step 3: Select start date for investing
    start_date = st.sidebar.date_input("Start date:", pd.to_datetime("2020-01-01"))

    # Step 4: Display the portfolio table
    st.subheader("Portfolio Overview")
    portfolio_data = pd.DataFrame({
        "Stock": tickers,
        "Weight": weights
    })
    st.table(portfolio_data)

    # Fetch stock data for selected stocks
    stock_data = fetch_stock_data(tickers, start_date)

    # Step 5: Calculate portfolio performance
    portfolio_performance = calculate_portfolio_performance(stock_data, weights)

    # Step 6: Plot portfolio performance
    st.subheader("Portfolio Performance")
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_performance.index, portfolio_performance, label="Portfolio Performance", color="blue")
    plt.title("Portfolio Performance Over Time")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    st.pyplot(plt)
else:
    st.write("Please select at least one stock.")