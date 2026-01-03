import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

import joblib
import os

# =========================================================
# LOAD DATA
# =========================================================
df = pd.read_csv("data/integrated_with_cost_index.csv")
print("✅ Dataset loaded:", df.shape)

# =========================================================
# DROP LEAKAGE
# =========================================================
DROP_COLS = [
    "product_id",
    "product_name",
    "material_id",
    "fragility_level",
    "cost_per_unit",
    "co2_emission_score",
    "sustainability_score_final"
]

df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

# =========================================================
# FEATURES
# =========================================================
FEATURES = [
    "category",
    "shipping_type",
    "material_type",
    "packaging_type",
    "supplier_region",
    "product_weight_kg",
    "fragility_index",
    "reusability_percent"
]

TARGET = "cost_impact_index"

X = df[FEATURES].copy()
y = df[TARGET]

# Encode categoricals
for col in X.select_dtypes(include="object").columns:
    X[col] = LabelEncoder().fit_transform(X[col].astype(str))

# =========================================================
# TRAIN–TEST SPLIT
# =========================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.40,
    stratify=y,
    random_state=42
)

# =========================================================
# VERY LIGHT NOISE
# =========================================================
X_train = X_train + np.random.normal(0, 0.015, X_train.shape)

# =========================================================
# RANDOM FOREST (FINAL CALIBRATION)
# =========================================================
model = RandomForestClassifier(
    n_estimators=180,
    max_depth=9,                    # 🔑 small depth increase
    min_samples_leaf=24,
    min_samples_split=55,
    class_weight={0: 1.0, 1: 1.0, 2: 1.25},  # 🔑 key fix
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# =========================================================
# EVALUATION
# =========================================================
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)

print("\n🌳 COST IMPACT MODEL (FINAL SUBMISSION)")
print("Accuracy:", acc)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# =========================================================
# SOFT COST IMPACT SCORE
# =========================================================
proba = model.predict_proba(X)

df["cost_impact_score"] = (
    0.2 * proba[:, 0] +
    0.5 * proba[:, 1] +
    0.8 * proba[:, 2]
)

df.to_csv("data/integrated_with_cost_score.csv", index=False)
print("✅ cost_impact_score saved")

# =========================================================
# SAVE MODEL
# =========================================================
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/cost_impact_model.pkl")
print("💾 cost_impact_model saved")
