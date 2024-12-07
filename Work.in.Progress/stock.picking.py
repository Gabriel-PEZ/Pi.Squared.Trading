import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Function to fetch stock data and statistics
def load_data(ticker):
    stock = yf.Ticker(ticker)
    return stock

def load_historical_data(stock, start_date):
    # Ensure date format compatibility
    start_date = pd.to_datetime(start_date, utc=True).tz_localize(None)
    # Get historical market data
    hist = stock.history(start=start_date)
    return hist

# Start of Streamlit UI
st.title("π² Trading")
st.header("Stock Picking")

# Input for stock symbol
ticker = st.text_input("Enter a stock symbol (e.g., AAPL for Apple):")

# Date picker for starting date
start_date = st.date_input("Choose the start date for the stock data:")

if st.button("Show Data") and ticker:
    stock = load_data(ticker)
    hist = load_historical_data(stock, start_date)

    if not hist.empty:
        st.subheader(f"Statistics for {ticker.upper()}")

        info = stock.info
        # Define the metrics to display
        metrics = {
            "Market Cap": f"${info.get('marketCap', 0) / 1e9:.2f}B",
            "Shares Out": f"{info.get('sharesOutstanding', 0) / 1e6:.2f}M",
            "EPS (ttm)": f"{info.get('trailingEps', 0):.2f}",
            "PE Ratio": f"{info.get('trailingPE', 0):.2f}"
        }

        # Additional details fetched from history
        additional_metrics = {
            "Volume": f"{hist['Volume'].iloc[-1]:,.0f}",
            "Open Price": f"${hist['Open'].iloc[0]:.2f}",
            "Previous Close": f"${hist['Close'].iloc[-1]:.2f}",
            "Day's Range": f"${hist['Low'].iloc[-1]:.2f} - ${hist['High'].iloc[-1]:.2f}",
            "Period Range": f"${hist['Close'].min():.2f} - ${hist['Close'].max():.2f}",
            "Beta": f"{info.get('beta', 0):.2f}"
        }

        # Display the metrics in two columns
        col1, col2 = st.columns(2)
        for idx, (key, value) in enumerate(metrics.items()):
            (col1 if idx % 2 == 0 else col2).metric(label=key, value=value)

        for idx, (key, value) in enumerate(additional_metrics.items()):
            (col1 if idx % 2 == 0 else col2).metric(label=key, value=value)

        # Plotting the stock graph
        fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                             open=hist['Open'],
                                             high=hist['High'],
                                             low=hist['Low'],
                                             close=hist['Close'])])
        fig.update_layout(title=f"Stock Prices for {ticker.upper()}",
                          xaxis_title="Date",
                          yaxis_title="Price",
                          height=800)  # Increased height for better visualization
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No data found for the given ticker and date range.")
else:
    st.info("Please enter a stock symbol and select a date to fetch data.")