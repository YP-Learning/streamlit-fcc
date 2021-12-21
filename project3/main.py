import streamlit as st
import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

# webscraping
@st.cache
def load_data(year):
    URL = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    html = pd.read_html(URL, header=0)
    df = html[0]
    
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    
    return playerstats.astype(str)

@st.cache
def cvt_df(df):
    return df.to_csv().encode("utf-8")

def main():
    st.title("NBA Player Stats Explorer")

    st.write("""
    This app performs simple webscraping of NBA player stats data!
    * **Python libraries:** pandas, streamlit
    * **Data source:** [Baskedball-refrence.com](https://www.basketball-refrence.com/).
    """)

    st.sidebar.header("User Input Features")
    selected_year = st.sidebar.selectbox("Year", list(reversed(range(1950, 2021))))

    stats = load_data(selected_year)

    teams = sorted(stats.Tm.unique())
    selected_teams = st.sidebar.multiselect("Teams: ", teams, teams)

    positions = sorted(stats.Pos.unique())
    selected_pos = st.sidebar.multiselect("Positions: ", positions, ["C", "PF", "PG", "SF", "SG"])

    # Filtering data
    stats_selected = stats[(stats.Tm.isin(selected_teams)) & (stats.Pos.isin(selected_pos))]

    st.write("## Display Player Stats of Selected Team(s)")
    st.text(f"Data Dimensions: {stats_selected.shape[0]}Columns, {stats_selected.shape[1]}rows")
    st.dataframe(stats_selected)

    col1, col2 = st.columns(2)

    col1.download_button(
        label="Download data as CSV",
        data=cvt_df(stats_selected),
        file_name=f'NBA_{selected_year}.csv',
        mime='text/csv',
    )

    # Heatmap
    if col2.button("Intercorrelation heatmap"):
        st.header('Intercorrelation Matrix Heatmap')
        stats_selected.to_csv('output.csv',index=False) # no idea how, but this works
        df = pd.read_csv('output.csv')

        corr = df.corr()
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask)] = True

        with sns.axes_style("dark"):
            fig, ax = plt.subplots(figsize=(7, 5))
            ax = sns.heatmap(corr, ax=ax, mask=mask, vmax=1, square=True)

        st.pyplot(fig)

if __name__ == '__main__':
    st.set_page_config(
        page_title="NBA Player Stats",
        page_icon=":basketball:"
    )

    main()
