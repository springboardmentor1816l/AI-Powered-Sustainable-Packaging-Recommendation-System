import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

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
    "fragility_level",
    "cost_per_unit",
    "sustainability_score_final",
    "co2_emission_score"
]

df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

# =========================================================
# FEATURES & TARGET
# =========================================================
TARGET = "co2_impact_index"

X = df.drop(columns=[TARGET])
y = df[TARGET]

# Encode categoricals
for col in X.select_dtypes(include="object").columns:
    X[col] = LabelEncoder().fit_transform(X[col].astype(str))

# =========================================================
# TRAIN–TEST SPLIT (HARDER)
# =========================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.40,        # 🔑 increased test size
    random_state=42,
    stratify=y
)

# =========================================================
# ADD LIGHT NOISE (REALISM)
# =========================================================
X_train = X_train + np.random.normal(0, 0.02, X_train.shape)

# =========================================================
# RANDOM FOREST (CALIBRATED)
# =========================================================
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,           # 🔑 shallower
    min_samples_leaf=500,  # 🔑 more conservative
    min_samples_split=800,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# =========================================================
# EVALUATION
# =========================================================
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)

print("\n🌳 CO₂ IMPACT MODEL (CALIBRATED)")
print("Accuracy:", acc)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# =========================================================
# SAVE SOFT CO₂ IMPACT SCORE
# =========================================================
proba = model.predict_proba(X)

df.loc[X.index, "co2_impact_score"] = (
    0.2 * proba[:, 0] +   # low impact
    0.5 * proba[:, 1] +   # medium
    0.8 * proba[:, 2]     # high impact
)

df.to_csv("data/integrated_with_co2_score.csv", index=False)
print("✅ co2_impact_score saved")

