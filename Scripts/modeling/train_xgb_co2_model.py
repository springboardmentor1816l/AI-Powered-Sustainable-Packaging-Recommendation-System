import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

# Ensure folders exist
os.makedirs("models", exist_ok=True)
os.makedirs("metrics", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# 1. Load data
X = pd.read_csv("data/model_ready/X_raw.csv")
y = pd.read_csv("data/model_ready/y_raw.csv")
# Drop text columns that XGBoost cannot process
X = X.drop(columns=[
    "product_name",
    "category",
    "shipping_type",
    "material_id",
    "industry_use_case"
])


# 3. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Initialize model
model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8
)

# 5. Train model
model.fit(X_train, y_train)

# 6. Evaluate model
pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, pred))
mae = mean_absolute_error(y_test, pred)
r2 = r2_score(y_test, pred)

# Save metrics
pd.DataFrame({
    "RMSE": [rmse],
    "MAE": [mae],
    "R2": [r2]
}).to_csv("metrics/co2_metrics.csv", index=False)

# 7. Save model
joblib.dump(model, "models/xgb_co2.joblib")

# 8. Save feature importance
importance = model.feature_importances_
pd.DataFrame({
    "feature_index": range(len(importance)),
    "importance": importance
}).to_csv("reports/feature_importance.csv", index=False)

print("✅ XGBoost CO₂ model training complete")
