import pandas as pd
from pathlib import Path
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# -------------------------------------------------
# Paths
# -------------------------------------------------
X_PATH = Path("../../data/model_input/X_raw.csv")
PIPELINE_OUT = Path("../../models/preprocessing/preprocessing_pipeline.pkl")
PIPELINE_OUT.parent.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------
X = pd.read_csv(X_PATH)

# -------------------------------------------------
# Column groups (FROZEN)
# -------------------------------------------------
numeric_features = [
    "product_weight_kg",
    "fragility_index",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",
    "recyclability_",
    "recycled_content_",
    "reusability_",
    "biodegradation_time_days",
    "endoflife_disposal_",
    "carbon_footprint_kg_co2unit",
    "waste_reduction_impact_",
    "sustainability_target_progress_",
    "annual_usage_units",
    "total_material_weight_tons",
    "supplier_sustainability_compliance_",
]

categorical_features = [
    "category",
    "shipping_type",
    "material_type",
    "packaging_type",
    "supplier_region",
    "recyclability_category"
]

binary_features = [
    "category_match_flag"
]

# -------------------------------------------------
# Transformers
# -------------------------------------------------
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

binary_transformer = "passthrough"

# -------------------------------------------------
# ColumnTransformer
# -------------------------------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
        ("bin", binary_transformer, binary_features)
    ],
    remainder="drop"
)

# -------------------------------------------------
# Fit pipeline (on full X for now; later only train split)
# -------------------------------------------------
preprocessor.fit(X)

# -------------------------------------------------
# Save pipeline
# -------------------------------------------------
joblib.dump(preprocessor, PIPELINE_OUT)

print("Preprocessing pipeline saved successfully")
