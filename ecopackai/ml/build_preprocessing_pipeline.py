import os
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer


# ============================
# Resolve paths safely
# ============================

BASE_DIR = os.path.dirname(__file__)                # ecopackai/ml
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # ecopackai
DATA_PATH = os.path.join(PROJECT_DIR, "data", "integrated_dataset.csv")

MODEL_DIR = os.path.join(PROJECT_DIR, "backend", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

PIPELINE_PATH = os.path.join(MODEL_DIR, "preprocessing_pipeline.pkl")


# ============================
# Load dataset
# ============================

df = pd.read_csv(DATA_PATH)


# ============================
# Define target columns
# ============================

TARGET_COLUMNS = [
    "cost_per_unit",
    "co2_emission_score"
]

print("Detected target columns:", TARGET_COLUMNS)


# ============================
# Drop targets (avoid leakage)
# ============================

X = df.drop(columns=TARGET_COLUMNS)


# ============================
# Drop problematic / redundant columns
# ============================

BAD_COLUMNS = [
    "carbon_footprint_kg_co2/unit"
]

X = X.drop(columns=[c for c in BAD_COLUMNS if c in X.columns])


# ============================
# Identify feature types
# ============================

numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_features = X.select_dtypes(include=["object"]).columns.tolist()


# ============================
# Build preprocessing pipelines
# ============================

numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ]
)


# ============================
# Fit preprocessing pipeline
# ============================

preprocessing_pipeline.fit(X)


# ============================
# Save preprocessing pipeline
# ============================

joblib.dump(preprocessing_pipeline, PIPELINE_PATH)

print(f"✅ preprocessing_pipeline.pkl saved at: {PIPELINE_PATH}")
