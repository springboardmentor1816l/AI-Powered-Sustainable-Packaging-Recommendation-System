import pandas as pd
import joblib
import os

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# ---------------- PATHS ----------------
DATA_PATH = "data/final/X_raw.csv"
PIPELINE_OUT = "models/preprocessing/preprocessing_pipeline.pkl"
SAMPLE_OUT = "data/model_ready/sample_transformed.csv"

# ---------------- DIRECTORIES ----------------
os.makedirs("models/preprocessing", exist_ok=True)
os.makedirs("data/model_ready", exist_ok=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATA_PATH)

# ---------------- FEATURE GROUPS ----------------
numeric_features = [
    "moisture_resistance_score",
    "thermal_resistance_score",
    "Load Handling Score",
    "CO2 Emission per kg (estimated)",
    "Biodegradation Time (days)",
    "Reusability (%)",
    "supplier_sustainability_compliance_pct",
    "Waste Reduction Impact (%)",
    "Sustainability Target Progress (%)",
    "Cost per Unit (USD)",
    "Annual Usage (units)",
    "Total Material Weight (tons)",
    "CII",
    "CEI",
    "MSS"
]

categorical_features = [
    "material_type",
    "Recyclability Category"
]

# ---------------- PIPELINES ----------------
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features),
    ],
    remainder="drop"
)

# ---------------- FIT ONLY ON TRAIN ----------------
X_train, _ = train_test_split(df, test_size=0.2, random_state=42)

X_train_transformed = preprocessor.fit_transform(X_train)

# ---------------- SAVE ----------------
joblib.dump(preprocessor, PIPELINE_OUT)

pd.DataFrame(X_train_transformed).head(50).to_csv(SAMPLE_OUT, index=False)

print("✅ Preprocessing pipeline created successfully")
print("Saved to:", PIPELINE_OUT)
print("Sample output saved to:", SAMPLE_OUT)
print("Total output features:", X_train_transformed.shape[1])
