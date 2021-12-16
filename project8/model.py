import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

penguins = pd.read_csv("./penguins_cleaned.csv")

df = penguins.copy()
target = 'species'
encode = [ 'sex', 'island' ]
target_mapper = { 'Adelie': 0, 'Chinstrap': 1, 'Gentoo': 2 }

for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df,dummy], axis=1)
    del df[col]

def target_encode(val):
    return target_mapper[val]

df['species'] = df['species'].apply(target_encode)

X = df.drop("species", axis=1)
y = df["species"]

clf = RandomForestClassifier()
clf.fit(X, y)

dump(clf, "model.joblib")
