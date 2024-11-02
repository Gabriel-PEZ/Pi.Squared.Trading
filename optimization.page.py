import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Function to fetch stock data with a custom date range
def fetch_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

# Function to calculate portfolio returns, volatility, and Sharpe ratio
def portfolio_metrics(weights, returns, cov_matrix):
    weights = np.array(weights)  # Ensure weights are numpy array
    portfolio_return = np.dot(returns, weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    sharpe_ratio = portfolio_return / portfolio_volatility  # Assumes risk-free rate = 0 for simplicity
    return portfolio_return, portfolio_volatility, sharpe_ratio

# Function to simulate random portfolios
def simulate_portfolios(data, num_portfolios, user_weights):
    daily_returns = data.pct_change().dropna()
    annual_returns = daily_returns.mean() * 252
    cov_matrix = daily_returns.cov() * 252
    num_stocks = len(data.columns)
    results = np.zeros((3 + num_stocks, num_portfolios + 1))  # Plus one for the user-defined portfolio

    # Simulate random portfolios
    for i in range(num_portfolios):
        weights = np.random.random(num_stocks)
        weights /= np.sum(weights)
        r, v, s = portfolio_metrics(weights, annual_returns, cov_matrix)
        results[:, i] = [r, v, s] + list(weights)

    # Include user-specified portfolio
    r, v, s = portfolio_metrics(user_weights, annual_returns, cov_matrix)
    results[:, -1] = [r, v, s] + user_weights  # Assign the last column for user portfolio

    columns = ['Return', 'Volatility', 'Sharpe Ratio'] + list(data.columns)
    portfolios = pd.DataFrame(results.T, columns=columns)
    return portfolios

# Function to plot the efficient frontier
def plot_efficient_frontier(portfolios):
    fig, ax = plt.subplots()
    # Exclude the last column which is the user portfolio
    scatter = ax.scatter(portfolios['Volatility'][:-1], portfolios['Return'][:-1], c=portfolios['Sharpe Ratio'][:-1], cmap='viridis', s=20, alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Sharpe Ratio')

    # Mark the user-defined portfolio
    user_portfolio = portfolios.iloc[-1]
    ax.scatter(user_portfolio['Volatility'], user_portfolio['Return'], color='black', marker='o', s=200, label='User Portfolio')

    # Identify and mark the portfolios with minimum volatility and maximum Sharpe ratio
    min_vol = portfolios.iloc[:-1].nsmallest(1, 'Volatility').iloc[0]
    max_sharpe = portfolios.iloc[:-1].nlargest(1, 'Sharpe Ratio').iloc[0]
    ax.scatter(min_vol['Volatility'], min_vol['Return'], color='blue', marker='*', s=200, label='Minimum Volatility')
    ax.scatter(max_sharpe['Volatility'], max_sharpe['Return'], color='red', marker='*', s=200, label='Maximum Sharpe Ratio')

    plt.title('Efficient Frontier with User Portfolio')
    plt.xlabel('Volatility (Standard Deviation)')
    plt.ylabel('Expected Return')
    plt.legend()
    return fig

# Streamlit UI setup
st.title('Custom Portfolio Optimization using Efficient Frontier')
start_date = st.date_input('Start Date', datetime(2010, 1, 1))
end_date = st.date_input('End Date', datetime.now())

# Dynamic stock selection and weight assignment
stocks = st.text_input('Enter stock tickers separated by space (e.g., AAPL GOOGL MSFT AMZN)').upper().split()
weights = []
if stocks:
    for ticker in stocks:
        weight = st.number_input(f'Weight for {ticker} (0-100%)', 0, 100, 25, key=ticker)
        weights.append(weight / 100)  # Normalize to 1 immediately

num_simulations = st.number_input('Number of Simulations', 1000, 100000, 10000)

if st.button('Calculate Efficient Frontier') and sum(weights) == 1.0:
    stock_data = fetch_data(stocks, start_date, end_date)
    if not stock_data.empty:
        portfolios = simulate_portfolios(stock_data, num_simulations, weights)
        fig = plot_efficient_frontier(portfolios)
        st.pyplot(fig)
        st.write("Minimum Volatility Portfolio:", portfolios.iloc[-3])
        st.write("Maximum Sharpe Ratio Portfolio:", portfolios.iloc[-2])
else:
    st.error("Total weights must sum to 100%.")