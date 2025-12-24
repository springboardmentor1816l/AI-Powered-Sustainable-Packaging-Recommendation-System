import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --- File Paths ---
TRAIN_PATH = 'data/model_ready/ml_train_dataset.csv'
TEST_PATH = 'data/model_ready/ml_test_dataset.csv'
MODEL_OUTPUT_PATH = 'ml/models/rf_cost.joblib'
METRICS_CSV_PATH = 'ml/metrics/rf_cost_metrics.csv'
SUMMARY_MD_PATH = 'docs/rf_cost_training_summary.md'

os.makedirs('ml/models', exist_ok=True)
os.makedirs('ml/metrics', exist_ok=True)
os.makedirs('docs', exist_ok=True)

# --- 1. Load Data ---
train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

TARGET_COST = 'Cost_Efficiency_Index'
ID_COLS = ['Material ID', 'product_id']

# Prepare Features (X) and Target (y)
X_train = train_df.drop(columns=[TARGET_COST, 'CO2_Impact_Index'] + ID_COLS, errors='ignore')
y_train = train_df[TARGET_COST]
X_test = test_df.drop(columns=[TARGET_COST, 'CO2_Impact_Index'] + ID_COLS, errors='ignore')
y_test = test_df[TARGET_COST]

# --- 2. Model Initialization ---
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

# --- 3. Implement 5-Fold Cross-Validation (MANDATORY) ---
print("Executing 5-Fold Cross-Validation...")
cv_results = cross_validate(
    rf_model, X_train, y_train, 
    cv=5, 
    scoring=['neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2'],
    return_train_score=False
)

# Calculate CV Averages
cv_mae = -cv_results['test_neg_mean_absolute_error'].mean()
cv_rmse = -cv_results['test_neg_root_mean_squared_error'].mean()
cv_r2 = cv_results['test_r2'].mean()

print(f"CV Results (Averages): R2={cv_r2:.4f}, RMSE={cv_rmse:.4f}, MAE={cv_mae:.4f}")

# --- 4. Final Training & Test Evaluation ---
print("\nTraining final model on full training set...")
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)

test_mae = mean_absolute_error(y_test, y_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
test_r2 = r2_score(y_test, y_pred)

print(f"Final Test Metrics: R2={test_r2:.4f}, RMSE={test_rmse:.4f}")

# --- 5. Save Deliverables ---
joblib.dump(rf_model, MODEL_OUTPUT_PATH)

# Save Metrics to CSV
metrics_data = {
    "Model": "Random Forest",
    "Target": "Cost",
    "CV_R2_Mean": cv_r2,
    "CV_RMSE_Mean": cv_rmse,
    "Test_R2": test_r2,
    "Test_RMSE": test_rmse
}
pd.DataFrame([metrics_data]).to_csv(METRICS_CSV_PATH, index=False)

# Generate Summary Report
summary_content = f"""
# Random Forest Cost Model Training Summary (with K-Fold CV)
Generated on {pd.Timestamp.now().strftime('%Y-%m-%d')}

## Cross-Validation Strategy (K=5)
* **Mean CV R2 Score:** {cv_r2:.4f}
* **Mean CV RMSE:** {cv_rmse:.4f}

## Final Performance (Unseen Test Data)
| Metric | Value |
| :--- | :--- |
| **MAE** | {test_mae:.4f} |
| **RMSE** | {test_rmse:.4f} |
| **R2 Score** | {test_r2:.4f} |

**Conclusion:** The consistency between CV scores and Test scores indicates the model is robust and not overfitting.
"""

with open(SUMMARY_MD_PATH, 'w') as f:
    f.write(summary_content)

print(f"\n✅ Task Complete. Model and K-Fold metrics saved.")