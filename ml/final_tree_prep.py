import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/integrated_dataset.csv")

for col in df.select_dtypes(include="object").columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

X = df.drop(columns=["sustainability_score"])
y = df["sustainability_score"]

print("STEP 7 DONE: RF & XGBoost data ready")
