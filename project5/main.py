from re import X
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(
    page_title="S&P 500 App",
    page_icon=":chart_with_upwards_trend:"
)
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("S&P 500 App")

st.write("""
This app retrieves the list of the S&P 500 (from Wikipedia) and its corresponding stock closing price (year-to-date)!

* **Python libraries**: pandas, streamlit, numpy, matplotlib, seaborn
* **Data source**: [Wikipedia](https://en.wikipedia.org/wiki/List_ofS%26P_500_companies).
""")

st.sidebar.header("User Input Features")

# Web scraping of S&P 500 data
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

@st.cache
def cvt_df(df):
    return df.to_csv().encode('utf-8')

@st.cache
def download_yf():
    return yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol
def price_plot(data, symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    # print(df)

    plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)

    # print("set")
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')

    return st.pyplot()

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

col1, col2 = st.columns(2)

col1.download_button(
    label="Download CSV",
    data=cvt_df(df_selected_sector),
    mime="text/csv",
    file_name="S_and_P_500.csv"
)

n_companies = st.sidebar.slider("Number of Companies: ", 1, 5)

if col2.button("View Plots"):
    data = download_yf()

    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:n_companies]:
        price_plot(data, i) 
