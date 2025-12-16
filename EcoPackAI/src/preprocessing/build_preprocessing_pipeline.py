"""
EcoPackAI — Build Preprocessing Pipeline (ColumnTransformer)

Module: Data Preparation & ML Readiness

Input:
- data/integrated_ecopack_dataset.csv

Output:
- models/preprocessing/preprocessing_pipeline.pkl
- data/model_ready/sample_transformed.csv
"""

import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split


# -------------------------------------------------------------------
# 1. Paths
# -------------------------------------------------------------------
RAW_DATA_PATH = "data/integrated_ecopack_dataset.csv"

PIPELINE_OUTPUT_PATH = "models/preprocessing/preprocessing_pipeline.pkl"
SAMPLE_OUTPUT_PATH = "data/model_ready/sample_transformed.csv"

os.makedirs("models/preprocessing", exist_ok=True)
os.makedirs("data/model_ready", exist_ok=True)


# -------------------------------------------------------------------
# 2. Load Dataset
# -------------------------------------------------------------------
print("📥 Loading dataset...")
df = pd.read_csv(RAW_DATA_PATH)


# -------------------------------------------------------------------
# 3. Target & Excluded Columns
# -------------------------------------------------------------------
TARGET_COLUMNS = [
    "recommended_material",
    "sustainability_score",
    "cost_efficiency_category"
]

EXCLUDED_COLUMNS = [
    "product_id",
    "material_id",
    "product_name"
] + TARGET_COLUMNS


# -------------------------------------------------------------------
# 4. Feature Groups (MATCHES DATASET EXACTLY)
# -------------------------------------------------------------------
NUMERIC_FEATURES = [
    "product_weight",
    "fragility_score",
    "moisture_sensitivity",
    "thermal_sensitivity",
    "expected_shelf_life_days",
    "material_cost_per_kg",
    "co2_emission_per_kg",
    "biodegradability_percent",
    "load_handling_score",
    "co2_impact_index",
    "cost_efficiency_index"
]

CATEGORICAL_FEATURES = [
    "product_category",
    "material_type",
    "recyclability_category",
    "supplier_region"
]

BINARY_FEATURES = [
    "hazardous_material_flag"
]


FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES + BINARY_FEATURES

print(f"✅ Total features used: {len(FEATURE_COLUMNS)}")


# -------------------------------------------------------------------
# 5. Validate Feature Presence (SAFETY CHECK)
# -------------------------------------------------------------------
missing_features = set(FEATURE_COLUMNS) - set(df.columns)
if missing_features:
    raise ValueError(f"❌ Missing features in dataset: {missing_features}")


# -------------------------------------------------------------------
# 6. Train-Test Split (FEATURES ONLY)
# -------------------------------------------------------------------
X = df[FEATURE_COLUMNS]

print("✂️ Splitting training and test data...")
X_train, X_test = train_test_split(
    X,
    test_size=0.2,
    random_state=42
)


# -------------------------------------------------------------------
# 7. Transformers
# -------------------------------------------------------------------
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
    ("encoder", OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    ))
])

binary_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent"))
])


# -------------------------------------------------------------------
# 8. ColumnTransformer
# -------------------------------------------------------------------
preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, NUMERIC_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ("bin", binary_transformer, BINARY_FEATURES)
    ],
    remainder="drop"
)

print("🧩 ColumnTransformer assembled")


# -------------------------------------------------------------------
# 9. Fit on TRAIN DATA ONLY
# -------------------------------------------------------------------
print("⚙️ Fitting preprocessing pipeline...")
X_train_processed = preprocessing_pipeline.fit_transform(X_train)

print("✅ Pipeline fitted successfully")


# -------------------------------------------------------------------
# 10. Transform Test Data
# -------------------------------------------------------------------
X_test_processed = preprocessing_pipeline.transform(X_test)


# -------------------------------------------------------------------
# 11. Save Pipeline
# -------------------------------------------------------------------
joblib.dump(preprocessing_pipeline, PIPELINE_OUTPUT_PATH)
print(f"💾 Pipeline saved to: {PIPELINE_OUTPUT_PATH}")


# -------------------------------------------------------------------
# 12. Save Sample Output
# -------------------------------------------------------------------
sample_df = pd.DataFrame(X_train_processed[:10])
sample_df.to_csv(SAMPLE_OUTPUT_PATH, index=False)
print(f"📊 Sample transformed data saved to: {SAMPLE_OUTPUT_PATH}")


# -------------------------------------------------------------------
# 13. Final Logs
# -------------------------------------------------------------------
print("\n✅ Preprocessing Pipeline Build Complete")
print(f"- Train shape (raw): {X_train.shape}")
print(f"- Train shape (processed): {X_train_processed.shape}")
print("- No missing values remain")
print("- Pipeline is production-ready")
