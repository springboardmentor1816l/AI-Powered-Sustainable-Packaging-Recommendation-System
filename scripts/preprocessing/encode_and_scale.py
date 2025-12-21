"""
Encode and scale regression features for EcoPackAI
--------------------------------------------------
Input  : data/final/X_regression_raw.csv
Output : data/final/X_regression_encoded_scaled.csv

- OneHotEncode categorical features
- StandardScale numeric features
- Save encoders for reuse
"""

import os
import pandas as pd
import joblib

from sklearn.preprocessing import OneHotEncoder, StandardScaler


# =========================
# Paths
# =========================
INPUT_PATH = "data/final/X_regression_raw.csv"
OUTPUT_PATH = "data/final/X_regression_encoded_scaled.csv"

ENCODER_DIR = "models/encoders"
SCALER_DIR = "models/scalers"

os.makedirs(ENCODER_DIR, exist_ok=True)
os.makedirs(SCALER_DIR, exist_ok=True)


# =========================
# Load dataset
# =========================
print("🚀 Encoding & scaling regression features")

X = pd.read_csv(INPUT_PATH)

# Normalize column names (SAFETY STEP)
X.columns = X.columns.str.strip().str.lower()

print("Initial shape:", X.shape)
print("Columns:", X.columns.tolist())


# =========================
# Feature groups
# =========================
CATEGORICAL_FEATURES = [
    "category",
    "shipping_type",
    "material_type",
    "packaging_type",
]

NUMERIC_FEATURES = [
    "product_weight_kg",
    "fragility_index",
    "recyclability_pct",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",
    "supplier_sustainability_compliance_pct",
    "sustainability_target_progress_pct",
]


# =========================
# Validate columns
# =========================
missing_cat = set(CATEGORICAL_FEATURES) - set(X.columns)
missing_num = set(NUMERIC_FEATURES) - set(X.columns)

if missing_cat:
    raise ValueError(f"Missing categorical columns: {missing_cat}")

if missing_num:
    raise ValueError(f"Missing numeric columns: {missing_num}")


# =========================
# Encode categorical
# =========================
ohe = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

X_cat = ohe.fit_transform(X[CATEGORICAL_FEATURES])

cat_feature_names = ohe.get_feature_names_out(CATEGORICAL_FEATURES)
X_cat_df = pd.DataFrame(X_cat, columns=cat_feature_names)

joblib.dump(ohe, f"{ENCODER_DIR}/ohe_encoder.pkl")

print("Encoded categorical shape:", X_cat_df.shape)


# =========================
# Scale numeric
# =========================
scaler = StandardScaler()
X_num = scaler.fit_transform(X[NUMERIC_FEATURES])

X_num_df = pd.DataFrame(X_num, columns=NUMERIC_FEATURES)

joblib.dump(scaler, f"{SCALER_DIR}/numeric_scaler.pkl")

print("Scaled numeric shape:", X_num_df.shape)


# =========================
# Combine
# =========================
X_final = pd.concat([X_num_df, X_cat_df], axis=1)

print("Final encoded shape:", X_final.shape)


# =========================
# Save
# =========================
X_final.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Saved encoded & scaled dataset to: {OUTPUT_PATH}")
