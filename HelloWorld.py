import streamlit as st
import yfinance as yf

st.write("Hello, World!")
data = yf.download("AAPL", start="2020-01-01", end="2020-12-31")
st.write(data)