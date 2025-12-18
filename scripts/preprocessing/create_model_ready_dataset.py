import os
import pandas as pd

IN_PATH = "data/final/materials_engineered.parquet"
OUT_PATH = "data/final/materials_model_ready.parquet"

print("🚀 Creating model-ready dataset")

df = pd.read_parquet(IN_PATH)

MODEL_FEATURES = [
    "CII",
    "CEI",
    "MSS",
    "moisture_resistance_score",
    "thermal_resistance_score",
    "Reusability (%)",
    "Waste Reduction Impact (%)",
    "Sustainability Target Progress (%)",
    "supplier_sustainability_compliance_pct"
]

df_model = df[MODEL_FEATURES]

os.makedirs("data/final", exist_ok=True)
df_model.to_parquet(OUT_PATH, index=False)

print("✅ Model-ready dataset saved to:", OUT_PATH)
