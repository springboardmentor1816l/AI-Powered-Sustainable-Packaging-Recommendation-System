import pandas as pd
import os

# Create output folder if not exists
os.makedirs("data/processed", exist_ok=True)

# Load cleaned datasets
cleaned = pd.read_csv("data/cleaned_datasets/materials_cleaned.csv")
engineered = pd.read_csv("data/processed/materials_final_scores.csv")

# -------- 1. Save Cleaned Data --------
cleaned.to_parquet("data/processed/materials_cleaned.parquet", index=False)

# -------- 2. Save Engineered Data --------
engineered.to_parquet("data/processed/materials_engineered.parquet", index=False)

# -------- 3. Save Model-Ready Data --------
# (For now same as engineered — later we will select ML features only)
engineered.to_parquet("data/processed/materials_model_ready.parquet", index=False)

print("✅ Parquet files generated successfully!")
