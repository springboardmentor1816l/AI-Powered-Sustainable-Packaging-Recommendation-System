import pandas as pd
import joblib
import os

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# Paths
X_PATH = "data/final/X_raw.csv"
y_PATH = "data/final/y_raw.csv"
PREPROCESSOR_PATH = "models/preprocessing/preprocessing_pipeline.pkl"
MODEL_OUTPUT_PATH = "models/trained/material_recommender.pkl"

os.makedirs("models/trained", exist_ok=True)

# Load data
X = pd.read_csv(X_PATH)
y = pd.read_csv(y_PATH)["recommended_material"]

# Load preprocessing pipeline
preprocessor = joblib.load(PREPROCESSOR_PATH)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

# Full pipeline
pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("model", model)
])

# Train
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
f1 = f1_score(y_test, y_pred, average="weighted")

print("✅ Pipeline trained successfully")
print("F1 score:", round(f1, 4))

# Save full pipeline
joblib.dump(pipeline, MODEL_OUTPUT_PATH)
print("Saved model to:", MODEL_OUTPUT_PATH)
