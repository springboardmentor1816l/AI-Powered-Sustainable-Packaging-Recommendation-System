import pandas as pd
import os

# Input (your cleaned CSV)
INPUT_CSV = "data/processed/cleaned_dataset.csv"

# Output directories
FINAL_DIR = "data/final/"
ARCHIVE_DIR = "archive/"

os.makedirs(FINAL_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

print("🔍 Loading cleaned dataset...")
df = pd.read_csv(INPUT_CSV)

# -------------------- EXPORT PARQUET FILES --------------------

print("📦 Exporting final_parquet files...")

# 1. Raw cleaned dataset (as parquet)
cleaned_parquet = f"{FINAL_DIR}materials_cleaned.parquet"
df.to_parquet(cleaned_parquet, index=False)

# If you have engineered features, you could separate them.
# But since you currently have only cleaned dataset, duplicate logic:
engineered_parquet = f"{FINAL_DIR}materials_engineered.parquet"
df.to_parquet(engineered_parquet, index=False)

model_ready_parquet = f"{FINAL_DIR}materials_model_ready.parquet"
df.to_parquet(model_ready_parquet, index=False)

print("✅ Parquet files exported successfully!")

# ------------------- ARCHIVE RAW VERSION ----------------------

print("🗄 Archiving raw dataset...")

archive_file = f"{ARCHIVE_DIR}cleaned_data_v1.parquet"
df.to_parquet(archive_file, index=False)

print("🎉 Dataset archived and exported.")
