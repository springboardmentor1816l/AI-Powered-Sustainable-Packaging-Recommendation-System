import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from pathlib import Path

# ------------------ PATHS ------------------
RAW_PATH = Path("EcopackAI/data/raw_datasets/materials/materials_raw.csv")
OUT_CLEAN_PATH = Path("EcopackAI/data/processed/cleaned_integrated_materials.csv")
OUT_REPORT_PATH = Path("EcopackAI/docs/missing_value_report.md")
OUT_MV_SUMMARY = Path("EcopackAI/data/processed/missing_values_summary.csv")

# Create folders if missing
OUT_CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
OUT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

# ------------------ LOAD DATA ------------------
df = pd.read_csv(RAW_PATH)

print("Loaded dataset:", RAW_PATH)
print("Shape:", df.shape)
print(df.info())

# ------------------ MISSING VALUES SUMMARY ------------------
mv = df.isna().sum().reset_index()
mv.columns = ["column", "missing_count"]
mv["missing_percent"] = (mv["missing_count"] / len(df)) * 100
mv = mv.sort_values(by="missing_count", ascending=False)

mv.to_csv(OUT_MV_SUMMARY, index=False)
print("Missing values summary saved:", OUT_MV_SUMMARY)

# ------------------ DEFINE COLUMN TYPES ------------------
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

# ------------------ IMPUTATION ------------------
# Numeric: median
num_imputer = SimpleImputer(strategy="median")
df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])

# Categorical: most frequent
cat_imputer = SimpleImputer(strategy="most_frequent")
df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

# Optional: replace still-empty text values
for col in categorical_cols:
    df[col] = df[col].replace("", "Unknown")

# ------------------ DROP VERY BAD ROWS (OPTIONAL) ------------------
# If row has too many missing fields in original data (before imputation),
# you can drop those rows. Here we keep it simple: no dropping.

# ------------------ FINAL VALIDATION ------------------
remaining_missing = df.isna().sum().sum()
print("Remaining missing values:", remaining_missing)

# Save cleaned dataset
df.to_csv(OUT_CLEAN_PATH, index=False)
print("Cleaned dataset saved:", OUT_CLEAN_PATH)

# ------------------ REPORT GENERATION ------------------
with open(OUT_REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("# Missing Value Report — EcoPackAI\n\n")
    f.write("## Dataset\n")
    f.write(f"- Input: `{RAW_PATH}`\n")
    f.write(f"- Output: `{OUT_CLEAN_PATH}`\n\n")

    f.write("## Missing Value Summary (Top Columns)\n")
    top_mv = mv.head(10)
    f.write(top_mv.to_markdown(index=False))
    f.write("\n\n")

    f.write("## Strategy Used\n")
    f.write("- Numeric columns: **Median imputation**\n")
    f.write("- Categorical columns: **Most frequent (mode) imputation**\n")
    f.write("- Empty categorical values replaced with: `Unknown`\n\n")

    f.write("## Validation\n")
    f.write(f"- Remaining missing values after cleaning: **{remaining_missing}**\n")

print("Missing value report generated:", OUT_REPORT_PATH)
