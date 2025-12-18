import pandas as pd
import os
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# -----------------------------
# Load dataset
# -----------------------------
data = pd.read_csv("data/processed/materials_final_scores.csv")

# -----------------------------
# Define column groups
# -----------------------------

NUMERIC_FEATURES = [
    "strength_mpa",
    "weight_capacity_kg",
    "biodegradability_percent",
    "co2_emission_kg_per_kg",
    "recyclability_percent",
    "cost_per_kg",
    "co2_impact_index",
    "cost_efficiency_index"
]

CATEGORICAL_FEATURES = [
    "material_type",
    "industry_use_case",
    "source_type",
    "recyclability_category"
]

EXCLUDED_COLUMNS = [
    "material_id",
    "material_suitability_score"  # target variable
]

TARGET_COLUMN = "material_suitability_score"

# -----------------------------
# Separate features and target
# -----------------------------
X = data.drop(columns=EXCLUDED_COLUMNS)
y = data[TARGET_COLUMN]

# -----------------------------
# Numeric pipeline
# -----------------------------
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# -----------------------------
# Categorical pipeline
# -----------------------------
categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# -----------------------------
# ColumnTransformer
# -----------------------------
preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, NUMERIC_FEATURES),
        ("cat", categorical_pipeline, CATEGORICAL_FEATURES)
    ],
    remainder="drop"
)

# -----------------------------
# Fit pipeline
# -----------------------------
preprocessing_pipeline.fit(X)

# -----------------------------
# Save pipeline
# -----------------------------
os.makedirs("models/preprocessing", exist_ok=True)
joblib.dump(
    preprocessing_pipeline,
    "models/preprocessing/preprocessing_pipeline.pkl"
)

print("✅ Preprocessing pipeline built and saved successfully")
