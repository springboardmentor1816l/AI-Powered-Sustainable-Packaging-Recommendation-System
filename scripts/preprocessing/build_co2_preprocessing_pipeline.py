import pandas as pd
import joblib
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# ---------------------------
# Paths
# ---------------------------
X_PATH = "data/final/X_co2_raw.csv"
PIPELINE_OUT = "models/preprocessing/co2_preprocessing_pipeline.pkl"

# ---------------------------
# Load data
# ---------------------------
X = pd.read_csv(X_PATH)

print("X shape:", X.shape)
print("Columns:", X.columns.tolist())

# ---------------------------
# Feature groups
# ---------------------------
NUMERIC_FEATURES = [
    "product_weight_kg",
    "fragility_index",
    "recyclability_pct",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",
    "supplier_sustainability_compliance_pct",
    "sustainability_target_progress_pct"
]

CATEGORICAL_FEATURES = [
    "shipping_type",
    "category",
    "packaging_type"
]

# ---------------------------
# Pipelines
# ---------------------------
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# ---------------------------
# ColumnTransformer
# ---------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, NUMERIC_FEATURES),
        ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
    ],
    remainder="drop"
)

# ---------------------------
# Fit pipeline
# ---------------------------
preprocessor.fit(X)

# ---------------------------
# Save pipeline
# ---------------------------
Path("models/preprocessing").mkdir(parents=True, exist_ok=True)
joblib.dump(preprocessor, PIPELINE_OUT)

print("✅ CO₂ preprocessing pipeline built successfully")
print(f"📁 Saved to: {PIPELINE_OUT}")
print("Output feature count:", preprocessor.transform(X).shape[1])
