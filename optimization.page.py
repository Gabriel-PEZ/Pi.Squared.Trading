import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import requests

# Function to fetch the 10-year Treasury yield from FRED API
def get_risk_free_rate(api_key="f1f1a2d3abcf1f08e76d3bc4fc1efd19"):
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'DGS10',
        'api_key': api_key,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data['observations'][0]['value']) / 100  # Convert to decimal
    except Exception as e:
        st.error(f"Error fetching risk-free rate: {e}")
        return 0.01  # Default to 1% if FRED API fails

# Function to fetch stock data
def fetch_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

# Function to calculate portfolio metrics
def portfolio_metrics(weights, returns, cov_matrix, risk_free_rate):
    weights = np.array(weights)
    portfolio_return = np.dot(returns, weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return portfolio_return, portfolio_volatility, sharpe_ratio

# Function to simulate random portfolios
def simulate_portfolios(data, num_portfolios, user_weights, risk_free_rate):
    daily_returns = data.pct_change().dropna()
    annual_returns = daily_returns.mean() * 252
    cov_matrix = daily_returns.cov() * 252
    num_stocks = len(data.columns)
    results = np.zeros((3 + num_stocks, num_portfolios + 1))

    for i in range(num_portfolios):
        weights = np.random.random(num_stocks)
        weights /= np.sum(weights)
        r, v, s = portfolio_metrics(weights, annual_returns, cov_matrix, risk_free_rate)
        results[:, i] = [r, v, s] + list(weights)

    # Include user portfolio
    r, v, s = portfolio_metrics(user_weights, annual_returns, cov_matrix, risk_free_rate)
    results[:, -1] = [r, v, s] + user_weights

    columns = ['Return', 'Volatility', 'Sharpe Ratio'] + list(data.columns)
    portfolios = pd.DataFrame(results.T, columns=columns)
    return portfolios

# Function to plot efficient frontier
def plot_efficient_frontier(portfolios):
    fig, ax = plt.subplots()
    scatter = ax.scatter(portfolios['Volatility'][:-1], portfolios['Return'][:-1], 
                         c=portfolios['Sharpe Ratio'][:-1], cmap='viridis', s=20, alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Sharpe Ratio')

    user_portfolio = portfolios.iloc[-1]
    ax.scatter(user_portfolio['Volatility'], user_portfolio['Return'], 
               color='black', marker='o', s=200, label='User Portfolio')

    min_vol = portfolios.iloc[:-1].nsmallest(1, 'Volatility').iloc[0]
    max_sharpe = portfolios.iloc[:-1].nlargest(1, 'Sharpe Ratio').iloc[0]
    ax.scatter(min_vol['Volatility'], min_vol['Return'], color='blue', marker='*', s=200, label='Minimum Volatility')
    ax.scatter(max_sharpe['Volatility'], max_sharpe['Return'], color='red', marker='*', s=200, label='Maximum Sharpe Ratio')

    plt.title('Efficient Frontier with User Portfolio')
    plt.xlabel('Volatility (Standard Deviation)')
    plt.ylabel('Expected Return')
    plt.legend()
    return fig

# Streamlit app
st.title('Custom Portfolio Optimization using Efficient Frontier')
start_date = st.date_input('Start Date', datetime(2010, 1, 1))
end_date = st.date_input('End Date', datetime.now())

# Using the default FRED API key
risk_free_rate = get_risk_free_rate()
st.write(f"Risk-Free Rate: {risk_free_rate * 100:.2f}%")

stocks = st.text_input('Enter stock tickers separated by space (e.g., AAPL GOOGL MSFT AMZN)').upper().split()
weights = []
if stocks:
    for ticker in stocks:
        weight = st.number_input(f'Weight for {ticker} (0-100%)', 0, 100, 25, key=ticker)
        weights.append(weight / 100)

num_simulations = st.number_input('Number of Simulations', 1000, 100000, 10000)

if st.button('Calculate Efficient Frontier') and sum(weights) == 1.0:
    stock_data = fetch_data(stocks, start_date, end_date)
    if not stock_data.empty:
        portfolios = simulate_portfolios(stock_data, num_simulations, weights, risk_free_rate)
        fig = plot_efficient_frontier(portfolios)
        st.pyplot(fig)
        st.write("Minimum Volatility Portfolio:", portfolios.iloc[:-1].nsmallest(1, 'Volatility'))
        st.write("Maximum Sharpe Ratio Portfolio:", portfolios.iloc[:-1].nlargest(1, 'Sharpe Ratio'))
else:
    st.error("Ensure total weights sum to 100% and stocks are entered.")