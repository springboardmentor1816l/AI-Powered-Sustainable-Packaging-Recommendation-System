import pandas as pd
import os

# ----------------------------
# Paths
# ----------------------------
INPUT_PATH = "data/processed/cleaned_dataset.csv"
OUTPUT_DIR = "data/model_input"

X_PATH = os.path.join(OUTPUT_DIR, "X_raw.csv")
Y_PATH = os.path.join(OUTPUT_DIR, "y_raw.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# Load dataset
# ----------------------------
print("📥 Loading cleaned dataset...")
df = pd.read_csv(INPUT_PATH)

print("Dataset shape:", df.shape)
print(df.head())

# ----------------------------
# Define Target
# ----------------------------
TARGET_COL = "Material Type"

y = df[TARGET_COL]

# ----------------------------
# Define Features
# ----------------------------
DROP_COLS = [
    "Material ID",
    "Material Type",
    "Recommended Packaging Use Cases"
]

X = df.drop(columns=DROP_COLS, errors="ignore")

# ----------------------------
# Save Outputs
# ----------------------------
X.to_csv(X_PATH, index=False)
y.to_csv(Y_PATH, index=False)

print("\n✅ Dataset preparation completed!")
print(f"Features saved to: {X_PATH}")
print(f"Target saved to: {Y_PATH}")

print("\n📊 Final Shapes:")
print("X shape:", X.shape)
print("y shape:", y.shape)

print("\n🎯 Target distribution:")
print(y.value_counts())
