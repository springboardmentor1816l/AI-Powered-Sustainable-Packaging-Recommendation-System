import pandas as pd

# Load datasets
cleaned = pd.read_csv("./data/processed/cleaned_integrated_materials.csv")
model_ready = pd.read_csv("./data/model_ready/materials_final_encoded.csv")

# Save parquet files
cleaned.to_parquet("./data/final/materials_cleaned.parquet", index=False)
model_ready.to_parquet("./data/final/materials_model_ready.parquet", index=False)

# materials_engineered.parquet will be generated after feature engineering materialization
