import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
import json, requests, time

st.set_page_config(
    page_title="Crypto Prize App",
    page_icon="./favicon.jpg",  # image from google images
    layout="wide"
)

st.title("Crypto Prize App")

image = Image.open("logo.jpg")
st.image(image, width=500)

st.write("This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the CoinMarketCap!")

with st.expander("About"):
    st.write("""
    * **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
    * **Data source:** [CoinMarketCap](http://coinmarketcap.com).
    * **Credit:** Web scraper adapted from the Medium article *[Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng](https://medium.com/@bryanf).
    """)

col1, col2 = st.columns([2, 1])

st.sidebar.header("Input Options")
currency_unit = st.sidebar.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

@st.cache
def cvt_df(df):
    return df.to_csv().encode("utf-8")

@st.cache
def load_data(currency_price_unit):
    response = requests.get("https://coinmarketcap.com")
    soup = BeautifulSoup(response.content, "html.parser")

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
  
    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    index = {
        "ID": 8,
        "Slug": 132,
        "Symbol": 133,

        "BTC.marketCap": 19,
        "BTC.percentChange1h": 22,
        "BTC.percentChange24h": 23,
        "BTC.percentChange7d": 26,
        "BTC.price": 28,
        "BTC.volume24h": 31,

        "ETH.marketCap": 38,
        "ETH.percentChange1h": 41,
        "ETH.percentChange24h": 42,
        "ETH.percentChange7d": 45,
        "ETH.price": 47,
        "ETH.volume24h": 50,
        
        "USD.marketCap": 57,
        "USD.percentChange1h": 60,
        "USD.percentChange24h": 61,
        "USD.percentChange7d": 64,
        "USD.price": 66,
        "USD.volume24h": 69,
    }

    for i in listings[1:]:
        coins[str(i[index["ID"]])] = i[index["Slug"]]  # 8 -> ID, 132 -> Slug

        coin_name.append(i[index["Slug"]])  # slug
        coin_symbol.append(i[index["Symbol"]])  # symbol
        price.append(i[index[f"{currency_price_unit}.price"]])
        percent_change_1h.append(i[index[f"{currency_price_unit}.percentChange1h"]])
        percent_change_24h.append(i[index[f"{currency_price_unit}.percentChange24h"]])
        percent_change_7d.append(i[index[f"{currency_price_unit}.percentChange7d"]])
        market_cap.append(i[index[f"{currency_price_unit}.marketCap"]])
        volume_24h.append(i[index[f"{currency_price_unit}.volume24h"]])

    return pd.DataFrame({
        "coin_name": coin_name,
        "coin_symbol": coin_symbol,
        "price": price,
        "percent_change_1h": percent_change_1h,
        "percent_change_24h": percent_change_24h,
        "percent_change_7d": percent_change_7d,
        "market_cap": market_cap,
        "volume_24h": volume_24h
    })

data = load_data(currency_unit)

coins_sorted = sorted(data["coin_symbol"])
selected_coins = st.sidebar.multiselect("Coins: ", coins_sorted, coins_sorted)

df_selected_coins = data[data["coin_symbol"].isin(selected_coins)]

## Sidebar - Number of coins to display
num_coin = st.sidebar.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coins[:num_coin]

## Sidebar - Percent change timeframe
percent_timeframe = st.sidebar.selectbox('Percent change time frame', ['7d','24h', '1h'])
percent_dict = {
    "7d": 'percent_change_7d', 
    "24h": 'percent_change_24h', 
    "1h": 'percent_change_1h'
}
selected_percent_timeframe = percent_dict[percent_timeframe]

sort_values = st.sidebar.checkbox("Sort values", True)

col1.subheader('Price Data of Selected Cryptocurrency')
col1.write('Data Dimension: ' + str(df_selected_coins.shape[0]) + ' rows and ' + str(df_selected_coins.shape[1]) + ' columns.')

col1.dataframe(df_selected_coins)

col1.download_button(
    label='Download all data',
    data=cvt_df(df_selected_coins),
    file_name="cryptocurrency_data.csv",
    mime="text/csv"
)

# Preparing data for Bar plot of % Price change
col1.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col1.dataframe(df_change)

# Conditional creation of Bar plot (time frame)
col2.subheader('Bar plot of % Price Change')

if sort_values:
    df_change = df_change.sort_values(by=[selected_percent_timeframe])

graph_title = {
    "percent_change_1h": "*1 hour period*",
    "percent_change_24h": "*24 hour period*",
    "percent_change_7d": "*7 days period*",
}

col2.write(graph_title[selected_percent_timeframe])

plt.figure(figsize=(5, 15))
plt.subplots_adjust(top = 1, bottom = 0)

df_change[selected_percent_timeframe].plot(
    kind = 'barh', 
    color = df_change[f"positive_{selected_percent_timeframe}"].map({True: 'g', False: 'r'})
)
col2.pyplot(plt)
