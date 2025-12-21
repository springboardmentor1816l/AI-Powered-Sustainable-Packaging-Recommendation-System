import pandas as pd
import os
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# -----------------------------
# Paths
# -----------------------------
X_PATH = "data/model_inputs/X_raw.csv"
PIPELINE_OUT = "models/preprocessing/preprocessing_pipeline.pkl"
SAMPLE_OUT = "data/model_ready/X_transformed_sample.csv"

os.makedirs("models/preprocessing", exist_ok=True)
os.makedirs("data/model_ready", exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
print("Loading X_raw...")
X = pd.read_csv(X_PATH)

# -----------------------------
# Column groups
# -----------------------------
numeric_features = [
    "product_weight_kg",
    "fragility_index",
    "Recyclability (%)",
    "Recycled Content (%)",
    "Reusability (%)",
    "Biodegradation Time (days)",
    "Waste Reduction Impact (%)",
    "Supplier Sustainability Compliance (%)",
    "Load Handling Score",
    "Moisture Resistance Score",
    "Thermal Resistance Score"
]

categorical_features = [
    "shipping_type",
    "category",
    "Material Type",
    "Packaging Type",
    "Recyclability Category",
    "Supplier Region"
]

# -----------------------------
# Pipelines
# -----------------------------
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# -----------------------------
# ColumnTransformer
# -----------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ],
    remainder="drop"
)

# -----------------------------
# Fit pipeline (ONLY on training-style data)
# -----------------------------
print("Fitting preprocessing pipeline...")
X_transformed = preprocessor.fit_transform(X)

# -----------------------------
# Save pipeline
# -----------------------------
joblib.dump(preprocessor, PIPELINE_OUT)
print(f"Pipeline saved → {PIPELINE_OUT}")

# -----------------------------
# Save sample transformed output
# -----------------------------
feature_names_num = numeric_features
feature_names_cat = preprocessor.named_transformers_["cat"]\
    .named_steps["encoder"]\
    .get_feature_names_out(categorical_features)

all_features = list(feature_names_num) + list(feature_names_cat)

X_transformed_df = pd.DataFrame(X_transformed, columns=all_features)
X_transformed_df.head(500).to_csv(SAMPLE_OUT, index=False)

print("Sample transformed data saved")
print(f"Final transformed shape: {X_transformed_df.shape}")
