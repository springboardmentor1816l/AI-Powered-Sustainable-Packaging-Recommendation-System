import pandas as pd
import os

# -----------------------------
# Step 1: Load filtered dataset
# -----------------------------
df = pd.read_csv(
    "data/processed/integrated_dataset_filtered.csv"
)

print("Filtered dataset shape:", df.shape)

# -----------------------------
# Step 2: Define target column
# -----------------------------
TARGET_COLUMN = "cost_per_kg"

# -----------------------------
# Step 3: Define columns to drop
# -----------------------------
DROP_COLUMNS = [
    "product_id",
    "product_name",
    "material_id",
    "material_type",
    TARGET_COLUMN
]

# -----------------------------
# Step 4: Create X and y
# -----------------------------
X = df.drop(columns=DROP_COLUMNS)
y = df[TARGET_COLUMN]

print("X shape:", X.shape)
print("y shape:", y.shape)

# -----------------------------
# Step 5: Save X_raw and y_raw
# -----------------------------
os.makedirs("data/model_inputs", exist_ok=True)

X.to_csv(
    "data/model_inputs/integrated_X_raw.csv",
    index=False
)

y.to_csv(
    "data/model_inputs/integrated_y_raw.csv",
    index=False
)

print("✅ Step 3 completed: Integrated X_raw & y_raw saved")
