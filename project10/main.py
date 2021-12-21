import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import pickle
from rdkit import Chem
from rdkit.Chem import Descriptors

# training nb
# https://github.com/dataprofessor/streamlit_freecodecamp/blob/main/app_10_regression_bioinformatics_solubility/solubility-web-app.ipynb

@st.cache
def load_model():
    return pickle.load(open('solubility_model.pkl', 'rb'))

def aromatic_proportion(m):
    aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
    aa_count = []

    for i in aromatic_atoms:
        if i == True:
            aa_count.append(1)

    AromaticAtom = sum(aa_count)
    HeavyAtom = Descriptors.HeavyAtomCount(m)

    AR = AromaticAtom/HeavyAtom
    return AR

def generate(smiles, verbose=False):

    moldata = [Chem.MolFromSmiles(e) for e in smiles]

    baseData = np.arange(1,1)
    i = 0

    for mol in moldata:
        row = np.array([Descriptors.MolLogP(mol),
                        Descriptors.MolWt(mol),
                        Descriptors.NumRotatableBonds(mol),
                        aromatic_proportion(mol)])

        baseData = row if i == 0 else np.vstack([baseData, row])
        i += 1

    columnNames=["MolLogP","MolWt","NumRotatableBonds","AromaticProportion"]
    descriptors = pd.DataFrame(data=baseData,columns=columnNames)

    return descriptors

def main():
    logo = Image.open('solubility-logo.jpg')
    st.image(logo, use_column_width=True)

    st.write("""
    # Molecular Solubility Prediction Web App
    This app predicts the **Solubility (LogS)** values of molecules!
    Data obtained from the John S. Delaney. [ESOL:  Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x). ***J. Chem. Inf. Comput. Sci.*** 2004, 44, 3, 1000-1005.
    ***
    """)

    st.header('User Input Features')

    # sample SMILES input
    SMILES_input = "NCCCC\nCCC\nCN"

    SMILES = st.text_area("SMILES input", SMILES_input)
    SMILES = "C\n" + SMILES 
    SMILES = SMILES.split('\n')

    st.header('Input SMILES')
    SMILES[1:] # Skips the dummy first item

    # Calculate molecular descriptors
    st.header('Computed molecular descriptors')
    X = generate(SMILES)
    X[1:] # Skips the dummy first item

    model = load_model()
    prediction = model.predict(X)

    st.header('Predicted LogS values')
    prediction[1:]  # print all except dummy

if __name__ == "__main__":
    main()
