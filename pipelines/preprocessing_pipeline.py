import os
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer

# =====================================================
# COLUMN GROUPS (MATCHING ACTUAL DATASET)
# =====================================================

# Numeric columns present in material_cleaned.csv
numeric_features = [
    "strength_mpa",
    "weight_capacity",
    "co2_emission_score",
    "biodegradability_percent",
    "recyclability_percent",
    "cost_per_kg"
]

# Categorical columns present in material_cleaned.csv
categorical_features = [
    "material_type",
    "indusrty_use_case"
]

# =====================================================
# PIPELINES
# =====================================================

# Numeric pipeline: impute + scale
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", MinMaxScaler())
])

# Categorical pipeline: impute + one-hot encode
categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# =====================================================
# COLUMN TRANSFORMER
# =====================================================

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ],
    remainder="drop"
)

# =====================================================
# SAVE PIPELINE
# =====================================================

os.makedirs("models/pipelines", exist_ok=True)

joblib.dump(
    preprocessor,
    "models/pipelines/preprocessing_pipeline.pkl"
)

print("✅ Preprocessing pipeline built and saved successfully")
