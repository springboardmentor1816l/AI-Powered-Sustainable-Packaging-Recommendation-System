import pandas as pd
import os

# -----------------------------
# Paths
# -----------------------------
INTEGRATED_PATH = "data/integrated/product_material_integrated.csv"
OUT_DIR = "data/model_inputs"

X_OUT = os.path.join(OUT_DIR, "X_raw.csv")
Y_OUT = os.path.join(OUT_DIR, "Y_raw.csv")

os.makedirs(OUT_DIR, exist_ok=True)

# -----------------------------
# Load integrated dataset
# -----------------------------
print("Loading integrated dataset...")
df = pd.read_csv(INTEGRATED_PATH)
print(f"Integrated shape: {df.shape}")

# -----------------------------
# Define TARGET variables (Y)
# -----------------------------
TARGET_COLUMNS = [
    "Cost per Unit (USD)",
    "Carbon Footprint (kg CO2/unit)"
]

# Optional target (uncomment later if needed)
# TARGET_COLUMNS.append("Material Suitability Score")

# -----------------------------
# Define FEATURE columns (X)
# -----------------------------
FEATURE_COLUMNS = [

    # ---- Product features ----
    "product_weight_kg",
    "fragility_index",
    "shipping_type",
    "category",

    # ---- Material features ----
    "Material Type",
    "Packaging Type",
    "Recyclability (%)",
    "Recyclability Category",
    "Recycled Content (%)",
    "Reusability (%)",
    "Biodegradation Time (days)",
    "CO2 Emission per kg (estimated)",
    "Waste Reduction Impact (%)",
    "Supplier Sustainability Compliance (%)",

    # ---- Performance scores ----
    "Load Handling Score",
    "Moisture Resistance Score",
    "Thermal Resistance Score",

    # ---- Operational context ----
    "Supplier Region"
]

# -----------------------------
# Validate column presence
# -----------------------------
missing_features = set(FEATURE_COLUMNS) - set(df.columns)
missing_targets = set(TARGET_COLUMNS) - set(df.columns)

if missing_features:
    raise ValueError(f"Missing feature columns: {missing_features}")

if missing_targets:
    raise ValueError(f"Missing target columns: {missing_targets}")

# -----------------------------
# Create X_raw and Y_raw
# -----------------------------
X_raw = df[FEATURE_COLUMNS].copy()
Y_raw = df[TARGET_COLUMNS].copy()

# -----------------------------
# Final sanity checks
# -----------------------------
assert X_raw.isnull().sum().sum() == 0, "X_raw contains missing values"
assert Y_raw.isnull().sum().sum() == 0, "Y_raw contains missing values"

# -----------------------------
# Save outputs
# -----------------------------
X_raw.to_csv(X_OUT, index=False)
Y_raw.to_csv(Y_OUT, index=False)

print("✅ X_raw and Y_raw successfully created")
print(f"X_raw shape: {X_raw.shape}")
print(f"Y_raw shape: {Y_raw.shape}")
print(f"Saved to: {OUT_DIR}")
