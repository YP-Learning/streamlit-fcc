import streamlit as st
import pandas as pd
import numpy as np
from joblib import load

@st.cache
def cvt_df(df):
    return df.to_csv().encode("utf-8")

@st.cache
def load_example_df():
    return pd.read_csv("https://raw.githubusercontent.com/YP-Learning/streamlit-fcc/main/project8/penguins_example.csv?token=ARG2APB5J5F2JI3UFMM5EK3BXPKAA")

def main():
    st.write("""
    # Penguin Prediction App
    This app predicts the **Palmer Penguin** species!

    Data obtained from the [palmerpenguins](https://github.com/allisonhorst/palmerpenguins) library in R by Allison Horst.

    ## User Input features
    Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).
    """)

    df_example = load_example_df()
    st.dataframe(df_example)

    c1, c2 = st.columns([3, 1])

    uploaded_file = c1.file_uploader(
        label = "CSV Input File",
        type = "csv",
    )

    c2.download_button(
        label = "Download Example.csv",
        file_name = "penguins_example.csv",
        data = cvt_df(df_example),
        mime = "text/csv"
    )

    if uploaded_file:
        df_example = pd.read_csv(uploaded_file)

    c1, c2, c3 = st.columns(3)

    islands = ["Biscoe", "Dream", "Torgersen"]
    sex_ = ["male", "female"]

    island = c1.selectbox("Island", islands, index=islands.index(df_example.island[0]))
    sex = c2.selectbox("Sex", sex_, index=sex_.index(df_example.sex[0]))
    bill_length_mm = c3.slider('Bill length (mm)', 32.1, 59.6, float(df_example.bill_length_mm[0]))
    bill_depth_mm = c3.slider('Bill depth (mm)', 13.1, 21.5, float(df_example.bill_depth_mm[0]))
    flipper_length_mm = c2.slider('Flipper length (mm)', 172.0, 231.0, float(df_example.flipper_length_mm[0]))
    body_mass_g = c1.slider('Body mass (g)', 2700.0, 6300.0, float(df_example.body_mass_g[0]))

    if uploaded_file:
        st.write("Using the following df for predictions")
        st.dataframe(df_example)

    penguins_raw = pd.read_csv('penguins_cleaned.csv')
    penguins = penguins_raw.drop(columns=['species'])
    df = pd.concat([df_example, penguins], axis=0)

    encode = ['sex', 'island']
    for col in encode:
        dummy = pd.get_dummies(df[col], prefix=col)
        df = pd.concat([df,dummy], axis=1)
        del df[col]

    df = df[:1] # Selects only the first row (the user input data)

    load_clf = load('model.joblib')

    # Apply model to make predictions
    prediction = load_clf.predict(df)
    prediction_proba = load_clf.predict_proba(df)


    st.subheader('Prediction')
    _, mcol, _ = st.columns(3)
    penguin_species = np.array(['Adelie','Chinstrap','Gentoo'])
    mcol.metric("Prediction", penguin_species[prediction][0], f"{max(prediction_proba[0])*100}%", delta_color="off")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Penguin Prediction APP",
        page_icon=":penguin:",
        # layout="wide",
    )
    main()
