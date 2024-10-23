import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

def fetch_stock_data(ticker, start_date):
    """ Fetches historical data of the specified stock from the start date to the current date. """
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date)
    return hist

def plot_stock_data(data):
    """ Plots the 'Close' price of the stock over time. """
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.title('Stock Close Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid(True)
    return plt

# Streamlit user interface
def main():
    st.title(f'$\pi^2$ Trading')

    # User inputs
    ticker = st.text_input('Enter the stock ticker symbol (e.g., AAPL):')
    start_date = st.date_input('Select start date:')

    if st.button('Fetch and Plot'):
        if ticker:
            data = fetch_stock_data(ticker, start_date)
            if not data.empty:
                fig = plot_stock_data(data)
                st.pyplot(fig)
            else:
                st.error('No data found for the given ticker and date range. Please try again.')
        else:
            st.error('Please enter a valid ticker symbol.')

if __name__ == '__main__':
    main()
