import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor


def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.write("""
    # Boston House Price Prediction App
    This app predicts the **Boston House Price**!
    """)
    st.write("---")

    st.header("Specify Input Parameters")

    # Loads the Boston House Price Dataset
    boston = datasets.load_boston()
    X = pd.DataFrame(boston.data, columns=boston.feature_names)
    y = pd.DataFrame(boston.target, columns=["MEDV"])

    cols = st.columns(3)
    feature_names = list(X.columns)
    features = {}

    for feature, idx in zip(feature_names, range(len(feature_names))):
        features[feature] = cols[idx % 3].slider(
            feature, X[feature].min(), X[feature].max(), X[feature].mean()
        )

    features = pd.DataFrame(features, index=[0])

    st.write("Specified Input Parameters")
    st.dataframe(features)
    st.write("---")

    # Regression
    regressor = RandomForestRegressor()
    regressor.fit(X, y)

    prediction = regressor.predict(features)

    # st.subheader('Prediction MEDV')
    _, mcol, _ = st.columns(3)
    mcol.metric("Prediction", f"{prediction[0]:.3f}", "MEDV")

    # Shap, for feature Importance 
    st.header("Feature Importance")
    st.write("Feature Importance based on SHAP values.")

    explainer = shap.TreeExplainer(regressor)
    shap_values = explainer.shap_values(X)

    fig = shap.summary_plot(shap_values, X)
    st.pyplot(fig, bbox_inches='tight')
    st.write('---')

    plt.title('Feature importance based on SHAP values (Bar)')
    fig = shap.summary_plot(shap_values, X, plot_type="bar")
    st.pyplot(fig, bbox_inches='tight')

if __name__ == "__main__":
    st.set_page_config(
        page_title="Boston House Prediction", 
        page_icon=":house:"
    )
    main()
