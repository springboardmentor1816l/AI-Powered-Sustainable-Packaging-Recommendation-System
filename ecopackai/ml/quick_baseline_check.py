# ============================================================
# EcoPackAI – Quick Baseline Model Check
# Linear Regression vs Regularized Decision Tree
# ============================================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_squared_error

# -----------------------------
# LOAD DATA
# -----------------------------
DATASET_PATH = "data/integrated_dataset_shap_clean.csv"
df = pd.read_csv(DATASET_PATH)

# -----------------------------
# DROP SAME FEATURES AS FINAL MODELS
# -----------------------------
DROP_FEATURES = [
    "product_id",
    "fragility_level",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score"
]

df = df.drop(columns=[c for c in DROP_FEATURES if c in df.columns])

# -----------------------------
# FEATURE ENGINEERING (SAME AS FINAL MODELS)
# -----------------------------
# Numeric binning (XGBoost/RF compatible)
conditions = [
    df["product_weight_kg"] <= 0.5,
    (df["product_weight_kg"] > 0.5) & (df["product_weight_kg"] <= 2.0),
    df["product_weight_kg"] > 2.0
]

df["product_weight_bin"] = np.select(conditions, [0, 1, 2], default=1)
df.drop(columns=["product_weight_kg"], inplace=True)

# Encode categorical features
categorical_cols = df.select_dtypes(include=["object"]).columns
for col in categorical_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

# -----------------------------
# SPLIT FEATURES / TARGET
# -----------------------------
TARGET = "sustainability_score"
X = df.drop(columns=[TARGET])
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ============================================================
# 1️⃣ LINEAR REGRESSION (BASELINE)
# ============================================================
lr = LinearRegression()
lr.fit(X_train, y_train)

lr_pred = lr.predict(X_test)
lr_r2 = r2_score(y_test, lr_pred)
lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))

# ============================================================
# 2️⃣ DECISION TREE (REGULARIZED BASELINE)
# ============================================================
dt = DecisionTreeRegressor(
    max_depth=5,
    min_samples_leaf=100,
    min_samples_split=200,
    random_state=42
)

dt.fit(X_train, y_train)

dt_pred = dt.predict(X_test)
dt_r2 = r2_score(y_test, dt_pred)
dt_rmse = np.sqrt(mean_squared_error(y_test, dt_pred))

# ============================================================
# RESULTS
# ============================================================
print("\n📊 QUICK BASELINE MODEL CHECK\n")

print("Linear Regression:")
print(f"  R² Score : {lr_r2:.4f}")
print(f"  RMSE     : {lr_rmse:.4f}\n")

print("Decision Tree (Regularized):")
print(f"  R² Score : {dt_r2:.4f}")
print(f"  RMSE     : {dt_rmse:.4f}")

print("\n✅ Use these baselines to justify Random Forest & XGBoost")

from sklearn.model_selection import cross_val_score

print("\n🔁 CROSS-VALIDATION CHECK (5-FOLD)\n")

# -------- Decision Tree CV --------
dt_cv_scores = cross_val_score(
    dt,
    X,
    y,
    cv=5,
    scoring="r2"
)

print("Decision Tree CV R² scores:", dt_cv_scores)
print("Decision Tree Mean R²:", dt_cv_scores.mean())
print("Decision Tree Std Dev:", dt_cv_scores.std())

# -------- Linear Regression CV --------
lr_cv_scores = cross_val_score(
    lr,
    X,
    y,
    cv=5,
    scoring="r2"
)

print("\nLinear Regression CV R² scores:", lr_cv_scores)
print("Linear Regression Mean R²:", lr_cv_scores.mean())
print("Linear Regression Std Dev:", lr_cv_scores.std())

