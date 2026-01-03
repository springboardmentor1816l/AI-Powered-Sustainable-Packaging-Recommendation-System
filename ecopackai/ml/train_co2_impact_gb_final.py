import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import GradientBoostingClassifier

# =========================================================
# LOAD DATA
# =========================================================
df = pd.read_csv("data/integrated_with_co2_index.csv")
print("✅ Dataset loaded:", df.shape)

# =========================================================
# DROP LEAKAGE
# =========================================================
DROP_COLS = [
    "product_id",
    "product_name",
    "material_id",
    "co2_emission_score",
    "sustainability_score_final",
    "cost_per_unit",
    "cost_impact_index"
]

df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

# =========================================================
# UNIFIED FEATURE SET
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

TARGET = "co2_impact_index"

X = df[FEATURES].copy()
y = df[TARGET]

# =========================================================
# ENCODE CATEGORICALS
# =========================================================
for col in X.select_dtypes(include="object").columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

# =========================================================
# TRAIN / TEST SPLIT
# =========================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.40,
    stratify=y,
    random_state=42
)

# =========================================================
# GRADIENT BOOSTING (FINAL ACCURACY PUSH)
# =========================================================
model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.07,
    max_depth=4,
    min_samples_leaf=25,
    subsample=0.9,
    random_state=42
)

model.fit(X_train, y_train)

# =========================================================
# EVALUATION
# =========================================================
y_pred = model.predict(X_test)

print("\n🌿 CO₂ IMPACT MODEL (GRADIENT BOOST – FINAL)")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# =========================================================
# SAVE MODEL
# =========================================================
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/co2_impact_model.pkl")

print("💾 co2_impact_model.pkl saved successfully")
