import streamlit as st
import altair as alt
import pandas as pd
from PIL import Image
from collections import Counter


st.title("DNA Nucleotide Count Web App")

logo = Image.open('dna-logo.jpg')
st.image(logo, use_column_width=True)

st.write("""
This app counts the nucleotide composition of query DNA!
""")

sample_DNA_sequences = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

st.header("Enter DNA sequences")
sequences = st.text_area("sequences input: ", sample_DNA_sequences, height=200, help="Enter the dna sequences, name of sequence <newline> sequences")
sequences = sequences.splitlines()
sequences = sequences[1:]  # ignore name
sequences = ''.join(sequences)

st.header("Input Sequenses: ")
st.text(sequences)

data = dict(Counter(sequences))
st.write("# Output \n### 1. Print Dictionary")
st.json(data)

st.write(f"""
### 2. Print text

There are {data['A']} Adenine (A)

There are {data['T']} Thymine (T)

There are {data['G']} Guanine (G)

There are {data['C']} Cytosine (C)


### 3. DataFrame
""")

df = pd.DataFrame({"Nucleotide": data.keys(), "Count": data.values()})
st.dataframe(df)

st.write("### 4. Chart")

chart = alt.Chart(df).mark_bar().encode(x="Nucleotide", y="Count")
chart = chart.properties(width = alt.Step(80))
st.write(chart)
