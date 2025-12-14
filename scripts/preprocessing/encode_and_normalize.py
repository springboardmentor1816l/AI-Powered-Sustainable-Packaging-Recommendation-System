import os
import pandas as pd
import joblib

from sklearn.preprocessing import (
    OrdinalEncoder,
    OneHotEncoder,
    MinMaxScaler,
    StandardScaler
)

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

INPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "cleaned_integrated_materials.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "model_ready", "materials_final_encoded.csv"
)

ENCODER_DIR = os.path.join(BASE_DIR, "models", "encoders")
SCALER_DIR = os.path.join(BASE_DIR, "models", "scalers")

os.makedirs(ENCODER_DIR, exist_ok=True)
os.makedirs(SCALER_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_PATH)

# --------------------------------------------------
# Column definitions (DEC 9 – Task 2)
# --------------------------------------------------

# Ordinal categorical columns
ordinal_cols = [
    "Material Type",
    "Packaging Type",
    "Supplier Region"
]

# Single-label nominal categorical
onehot_cols = [
    "Recyclability Category"
]

# Multi-label categorical columns (semicolon separated)
multilabel_cols = [
    "Suitable Product Categories",
    "Recommended Packaging Use Cases"
]

# Numeric columns – normalization strategy (Option B)
numeric_minmax = [
    "Waste Reduction Impact (%)",
    "Recyclability (%)"
]

numeric_standard = [
    "Carbon Footprint (kg CO2/unit)",
    "Biodegradation Time (days)"
]

# --------------------------------------------------
# Safety checks
# --------------------------------------------------

missing_cols = (
    set(ordinal_cols + onehot_cols + multilabel_cols +
        numeric_minmax + numeric_standard)
    - set(df.columns)
)

if missing_cols:
    raise ValueError(f"Missing expected columns: {missing_cols}")

# --------------------------------------------------
# Multi-label One-Hot Encoding (MUST COME FIRST)
# --------------------------------------------------

def multilabel_ohe(series: pd.Series, prefix: str) -> pd.DataFrame:
    """
    Perform multi-label one-hot encoding on a semicolon-separated column.
    """
    series = series.fillna("").astype(str)
    dummies = series.str.get_dummies(sep=";")
    dummies.columns = [f"{prefix}_{c.strip()}" for c in dummies.columns]
    return dummies


ml_product = multilabel_ohe(
    df["Suitable Product Categories"], "product_cat"
)

ml_usecase = multilabel_ohe(
    df["Recommended Packaging Use Cases"], "usecase"
)

# Persist multi-label feature names (used during inference)
joblib.dump(
    list(ml_product.columns),
    os.path.join(ENCODER_DIR, "multilabel_encoder_products.pkl")
)

joblib.dump(
    list(ml_usecase.columns),
    os.path.join(ENCODER_DIR, "multilabel_encoder_usecases.pkl")
)

# Drop original multi-label columns
df = df.drop(columns=multilabel_cols)

# Append encoded features
df = pd.concat([df, ml_product, ml_usecase], axis=1)

# --------------------------------------------------
# Ordinal Encoding (single-value categorical)
# --------------------------------------------------

ordinal_encoder = OrdinalEncoder(
    handle_unknown="use_encoded_value",
    unknown_value=-1
)

df[ordinal_cols] = ordinal_encoder.fit_transform(df[ordinal_cols])

joblib.dump(
    ordinal_encoder,
    os.path.join(ENCODER_DIR, "ordinal_encoder.pkl")
)

# --------------------------------------------------
# One-Hot Encoding (single-label nominal)
# --------------------------------------------------

ohe = OneHotEncoder(
    sparse_output=False,
    handle_unknown="ignore"
)

ohe_encoded = ohe.fit_transform(df[onehot_cols])

ohe_df = pd.DataFrame(
    ohe_encoded,
    columns=ohe.get_feature_names_out(onehot_cols),
    index=df.index
)

joblib.dump(
    ohe,
    os.path.join(ENCODER_DIR, "onehot_encoder_recyclability.pkl")
)

df = df.drop(columns=onehot_cols)
df = pd.concat([df, ohe_df], axis=1)

# --------------------------------------------------
# Numeric Normalization (Option B)
# --------------------------------------------------

scaler_minmax = MinMaxScaler()
df[numeric_minmax] = scaler_minmax.fit_transform(df[numeric_minmax])

scaler_standard = StandardScaler()
df[numeric_standard] = scaler_standard.fit_transform(df[numeric_standard])

joblib.dump(
    {
        "minmax": scaler_minmax,
        "standard": scaler_standard
    },
    os.path.join(SCALER_DIR, "numeric_scaler.pkl")
)

# --------------------------------------------------
# Final validation
# --------------------------------------------------

if df.isnull().sum().sum() != 0:
    raise ValueError("Null values detected after preprocessing")

# --------------------------------------------------
# Save final dataset
# --------------------------------------------------

df.to_csv(OUTPUT_PATH, index=False)

print(f"Final dataset saved at: {OUTPUT_PATH}")
