import pandas as pd
import joblib

print("Loading dataset...")
X = pd.read_csv("data/final/X_raw.csv")

print("Saving cost model features (drop_first=True)...")
X_cost = pd.get_dummies(X, drop_first=True)
joblib.dump(X_cost.columns.tolist(), "ml/models/rf_cost_features.joblib")

print("Saving CO2 model features (drop_first=True)...")
X_co2 = pd.get_dummies(X.drop(columns=["material_type"]), drop_first=True)
joblib.dump(X_co2.columns.tolist(), "ml/models/xgb_co2_features.joblib")

print("✅ Feature lists RESAVED correctly")
