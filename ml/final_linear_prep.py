import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/integrated_dataset.csv")

# Encode categoricals
df = pd.get_dummies(df, drop_first=True)

X = df.drop(columns=["sustainability_score"])
y = df["sustainability_score"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("STEP 6 DONE: Linear Regression data ready")
