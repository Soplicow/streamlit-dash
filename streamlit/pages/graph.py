import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

@st.cache_data
def get_stock_data(symbol, period="1y", interval="1d"):
    """Fetch stock data from Yahoo Finance."""
    try:
        stock_data = yf.Ticker(symbol)
        stock_history = stock_data.history(period = period, interval = interval)
        if stock_history.empty:
            return None

        return stock_history
    except Exception as e:
        return None

st.write("# Graph Page")
st.write("This is the graph page.")

st.write("You can use this page to visualize stock market data.")
st.write("Select a stock symbol, time period, and interval to view its historical data and graphs.")

st.divider()

st.write("## Search for a stock symbol")
stock_symbol = st.text_input("Enter stock symbol (e.g., AAPL, MSFT):", "AAPL", help="Start typing to see suggestions.")
suggested_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NFLX", "NVDA", "BABA", "INTC"]
if stock_symbol not in suggested_symbols:
    st.warning("Suggested symbols: " + ", ".join(suggested_symbols))
time_period = st.selectbox("Select time period:", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"])
interval = st.selectbox("Select interval:", ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1mo"])

if st.button("Search"):
    stock_data = get_stock_data(stock_symbol, time_period, interval)
    if stock_data is not None:
        st.divider()
        st.write(f"### You selected: {stock_symbol}")
        st.write("## Historical Data")
        st.dataframe(stock_data)

        try:
            st.divider()
            st.write("## Stock Price Candle Graph")
            fig = go.Figure(data=[go.Candlestick(
                x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close']
            )])
            fig.update_layout(title=f"Candlestick Chart for {stock_symbol}", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error plotting data: {e}")
    else:
        st.warning("No data available for the selected stock symbol.")