import pandas as pd 
import joblib
import numpy as np
from  xgboost import XGBRegressor
from sklearn.model_selection import cross_validate,train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score

# 1. Load Data and Preprocessing Pipeline

data=pd.read_csv("data/final/integrated_dataset.csv")
pipeline = joblib.load("models/preprocessing/preprocessing_pipeline.pkl")

y_co2=data[["CO2_Impact_Index"]]
exclude_cols = ['product_id', 'Material ID', 'product_name', 'Cost_Efficiency_Index', 'CO2_Impact_Index']
X_raw = data.drop(columns=[col for col in exclude_cols if col in data.columns])
X_processed = pipeline.transform(X_raw)

# 2. Train-Test Split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y_co2, test_size=0.2, random_state=42
)

# 3. Initialize and Train XGBoost
print("Training XGBoost Model for CO2 Prediction...")
xgb_model = XGBRegressor(
    objective='reg:squarederror',
    n_estimators=100,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

print("Executing 5-Fold Cross-Validation for CO2 model...")
cv_results = cross_validate(
    xgb_model, X_processed, y_co2.values.ravel(), 
    cv=5, 
    scoring=['neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2']
)
# Averages
cv_mae = -cv_results['test_neg_mean_absolute_error'].mean()
cv_rmse = -cv_results['test_neg_root_mean_squared_error'].mean()
cv_r2 = cv_results['test_r2'].mean()

print(f"CV Results: R2={cv_r2:.4f}, RMSE={cv_rmse:.4f}")

# 4.Model Training

xgb_model.fit(X_train,y_train)

# 4. Model Evaluation

y_pred=xgb_model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Results: R2={r2:.4f}, RMSE={rmse:.4f}, MAE={mae:.4f}")


# Save the model
joblib.dump(xgb_model, "models/xgb_co2.joblib")

# Save Metrics
metrics_df = pd.DataFrame([{
    "Model": "XGBoost",
    "Target": "CO2",
    "CV_R2": cv_r2,
    "Test_R2": r2 ,
    "Test_RMSE": rmse
}])
metrics_df.to_csv('ml/metrics/co2_metrics.csv', index=False)

# Feature Importance
feature_names = pipeline.get_feature_names_out()
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': xgb_model.feature_importances_
}).sort_values(by='Importance', ascending=False)
importance_df.to_csv('docs/reports/feature_importance.csv', index=False)


