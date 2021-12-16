import random
import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier


def get_model():
    X, y = iris.data, iris.target
    random.seed(42)
    clf = RandomForestClassifier()

    return clf.fit(X, y)

st.write("""
# Simple Iris Flower Prediction App
This app predicts the **Iris flower** type!
""")

# load the iris data
iris = load_iris()

st.header("Input Features")

col1, col2 = st.columns(2)

sepal_length = col1.slider('Sepal length', 4.3, 7.9, 5.4)
sepal_width = col1.slider('Sepal width', 2.0, 4.4, 3.4)

petal_length = col2.slider('Petal length', 1.0, 6.9, 1.3)
petal_width = col2.slider('Petal width', 0.1, 2.5, 0.2)

df = pd.DataFrame({
    "sepal_length": sepal_length,
    "sepal_width": sepal_width,
    "petal_length": petal_length,
    "petal_width": petal_width
}, index=[0])

st.subheader("User Input Parameters")
st.dataframe(df)

clf = get_model()

prediction = clf.predict(df)
pred_proba = clf.predict_proba(df)

st.subheader('Class labels and their corresponding index number')
st.write(iris.target_names)

st.markdown("---")

_, mcol, _ = st.columns(3)
mcol.metric("Prediction", iris.target_names[prediction][0], max(pred_proba[0]), delta_color="off")
