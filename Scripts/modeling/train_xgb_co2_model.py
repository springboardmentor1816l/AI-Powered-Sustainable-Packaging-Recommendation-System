import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

# --------------------------------------------------
# 1. PATH SETUP
# --------------------------------------------------
os.makedirs("models", exist_ok=True)
os.makedirs("metrics", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("docs", exist_ok=True)

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------
df_X = pd.read_csv("data/model_ready/X_raw.csv")
df_y = pd.read_csv("data/model_ready/y_raw.csv")

# PDF requires CO₂ as target
y = df_y["co2_emission_score"]

X = df_X.drop(columns=[
    "product_name",
    "category",
    "shipping_type",
    "material_id",
    "industry_use_case"
], errors="ignore")

# --------------------------------------------------
# 3. TRAIN / TEST SPLIT
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------------------------------
# 4. MODEL
# --------------------------------------------------
model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------------------------------
# 5. EVALUATION
# --------------------------------------------------
pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, pred))
mae = mean_absolute_error(y_test, pred)
r2 = r2_score(y_test, pred)

metrics_df = pd.DataFrame({
    "RMSE": [rmse],
    "MAE": [mae],
    "R2": [r2]
})

metrics_df.to_csv("metrics/co2_metrics.csv", index=False)

# --------------------------------------------------
# 6. SAVE MODEL
# --------------------------------------------------
joblib.dump(model, "models/xgb_co2.joblib")

# --------------------------------------------------
# 7. FEATURE IMPORTANCE
# --------------------------------------------------
importance = model.feature_importances_

pd.DataFrame({
    "feature": X.columns,
    "importance": importance
}).to_csv("reports/feature_importance.csv", index=False)

# --------------------------------------------------
# 8. DAY-15 DOCUMENTATION
# --------------------------------------------------
REPORT_PATH = "docs/co2_model_report.md"
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(f"""
# XGBoost CO₂ Prediction Model — Day 15

**Model:** XGBoost Regressor  
**Target:** CO₂ Emission Score  

## Performance
- RMSE: {rmse:.4f}
- MAE: {mae:.4f}
- R2 Score: {r2:.6f}

## Purpose
This model predicts CO₂ emission impact of packaging choices to support sustainable material recommendation.
""")

print("✅ XGBoost CO₂ model training complete (Day-15 compliant)")
