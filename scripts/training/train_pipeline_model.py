import os
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# -------------------------------------------------
# Paths
# -------------------------------------------------
X_PATH = "data/final/X_raw.csv"
Y_PATH = "data/final/y_raw.csv"
MODEL_OUTPUT_PATH = "ml/models/model_pipeline.joblib"

os.makedirs("ml/models", exist_ok=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------
print("📥 Loading data...")

X = pd.read_csv(X_PATH)
y = pd.read_csv(Y_PATH)["material_type"]

# -------------------------------------------------
# Identify column types dynamically
# -------------------------------------------------
numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

print("🔢 Numeric features:", numeric_features)
print("🔤 Categorical features:", categorical_features)

# -------------------------------------------------
# Preprocessing pipelines
# -------------------------------------------------
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

# -------------------------------------------------
# Model
# -------------------------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

# -------------------------------------------------
# Full pipeline
# -------------------------------------------------
pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("model", model)
])

# -------------------------------------------------
# Train / test split
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------------------------------
# Train
# -------------------------------------------------
print("🚀 Training model...")
pipeline.fit(X_train, y_train)

# -------------------------------------------------
# Evaluate
# -------------------------------------------------
y_pred = pipeline.predict(X_test)
f1 = f1_score(y_test, y_pred, average="weighted")

print("✅ Pipeline trained successfully")
print("📊 F1 score:", round(f1, 4))

# -------------------------------------------------
# Save pipeline (backend will load this)
# -------------------------------------------------
joblib.dump(pipeline, MODEL_OUTPUT_PATH)

print(f"💾 Model pipeline saved at: {MODEL_OUTPUT_PATH}")
