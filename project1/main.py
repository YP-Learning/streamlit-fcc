import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple Stock Price App

Shown are the stock _closing price_ and _volume_ of Google!

""")

ticker_symbol = 'goog'

ticker_data = yf.Ticker(ticker_symbol)

ticker_df = ticker_data.history(period="1d", start="2010-5-31", end="2021-5-31")

st.line_chart(ticker_df.Close)
st.line_chart(ticker_df.Volume)
