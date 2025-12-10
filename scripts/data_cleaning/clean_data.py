import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import os

RAW_PATH = "ecopack_ai.csv"
OUTPUT_PATH = "data/processed/cleaned_dataset.csv"
REPORT_PATH = "docs/missing_value_report.md"

os.makedirs("data/processed", exist_ok=True)
os.makedirs("docs", exist_ok=True)

print("📥 Loading dataset...")
df = pd.read_csv(RAW_PATH)

# -------------------------------
# 1️⃣ Missing Value Inspection
# -------------------------------
missing = df.isna().sum()
print("\n🔍 Missing Value Summary:\n", missing)

# Save report
with open(REPORT_PATH, "w") as f:
    f.write("# Missing Value Report\n\n")
    f.write("## Missing Values Per Column\n")
    f.write(missing.to_string())
    f.write("\n\n---\n")

# -------------------------------
# 2️⃣ Separate Numeric & Categorical
# -------------------------------
numeric_cols = df.select_dtypes(include=[np.number]).columns
categorical_cols = df.select_dtypes(exclude=[np.number]).columns

print("\nNumeric Columns:", list(numeric_cols))
print("Categorical Columns:", list(categorical_cols))

# -------------------------------
# 3️⃣ Imputation Logic
# -------------------------------
num_imputer = SimpleImputer(strategy="median")
cat_imputer = SimpleImputer(strategy="most_frequent")

df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])
df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

# -------------------------------
# 4️⃣ Remove rows still missing
# -------------------------------
df.dropna(inplace=True)

print("\n✔ Missing values cleaned!")
print("Shape after cleaning:", df.shape)

# -------------------------------
# 5️⃣ Export Clean Dataset
# -------------------------------
df.to_csv(OUTPUT_PATH, index=False)
print(f"\n📤 Cleaned dataset saved to: {OUTPUT_PATH}")
