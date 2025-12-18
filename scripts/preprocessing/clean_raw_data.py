import os
import pandas as pd

IN_PATH = "data/interim/materials_standardized.csv"
OUT_PATH = "data/interim/materials_cleaned.csv"

print("🚀 Starting data cleaning (standardized → cleaned)")

df = pd.read_csv(IN_PATH)
print("Initial shape:", df.shape)

df = df.drop_duplicates()
print("After dropping duplicates:", df.shape)

string_cols = df.select_dtypes(include="object").columns
df[string_cols] = df[string_cols].apply(lambda x: x.str.strip())

mandatory_cols = [
    "Cost per Unit (USD)",
    "CO2 Emission per kg (estimated)",
    "Biodegradation Time (days)",
    "moisture_resistance_score",
    "thermal_resistance_score"
]

print("Mandatory columns:", mandatory_cols)
print("Available columns:", df.columns.tolist())

df = df.dropna(subset=mandatory_cols)
print("After dropping null mandatory rows:", df.shape)

df = df[df["Cost per Unit (USD)"] > 0]
df = df[df["CO2 Emission per kg (estimated)"] >= 0]
df = df[df["Biodegradation Time (days)"] >= 1]
df = df[df["moisture_resistance_score"].between(1, 10)]
df = df[df["thermal_resistance_score"].between(1, 10)]

print("After numeric constraints:", df.shape)

os.makedirs("data/interim", exist_ok=True)
df.to_csv(OUT_PATH, index=False)

print("✅ Cleaned dataset saved to:", OUT_PATH)
