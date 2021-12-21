import streamlit as st
import os

projects = {
    "Simple Stock Price App": "project1",
    "DNA count Web App": "project2",
    "NBA Player Stats": "project3",
    "NFL Football Stats": "project4",
    "S&P 500 App": "project5",
    "Crypto Prize App": "project6",
    "Iris Flower Prediction": "project7",
    "Penguin Prediction App": "project8",
    "Boston House Prediction": "project9",
    "Molecular Solubility Prediction Web App": "project10"
}

selected_project = st.sidebar.selectbox("Project: ", list(projects.keys()))

with st.expander("Credits"):
    st.markdown("""<iframe width="560" height="315" src="https://www.youtube.com/embed/JwSS70SZdyM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>""", unsafe_allow_html=True)
    st.markdown("This Project was created by getting inspired by the above video, #CodeFirst and then video.")

selected_project = projects[selected_project]
if selected_project == "project1":
    from project1 import main

elif selected_project == "project2":
    from project2 import main

elif selected_project == "project3":
    from project3 import main

elif selected_project == "project4":
    from project4 import main

elif selected_project == "project5":
    from project5 import main

elif selected_project == "project6":
    from project6 import main

elif selected_project == "project7":
    from project7 import main

elif selected_project == "project8":
    from project8 import main

elif selected_project == "project9":
    from project9 import main

elif selected_project == "project10":
    from project10 import main

try:
    os.chdir(selected_project)
    print(os.getcwd())
    main.main()
finally:
    os.chdir("../")
