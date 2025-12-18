import pandas as pd
from sklearn.model_selection import train_test_split
import os

# ---------------- Load model-ready data ----------------
df = pd.read_parquet("data/processed/materials_model_ready.parquet")

# ---------------- Define target & features ----------------
TARGET = "material_suitability_score"

X = df.drop(columns=[TARGET])
y = df[TARGET]   # this is a Series

# ---------------- Train-Test Split ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------- Save outputs ----------------
os.makedirs("data/model_inputs", exist_ok=True)

X_train.to_parquet("data/model_inputs/X_train.parquet", index=False)
X_test.to_parquet("data/model_inputs/X_test.parquet", index=False)

# 🔹 Convert Series → DataFrame before saving
y_train.to_frame(name=TARGET).to_parquet(
    "data/model_inputs/y_train.parquet", index=False
)
y_test.to_frame(name=TARGET).to_parquet(
    "data/model_inputs/y_test.parquet", index=False
)

print("✅ Train-test split completed successfully")
print(f"Train size: {X_train.shape}")
print(f"Test size: {X_test.shape}")
