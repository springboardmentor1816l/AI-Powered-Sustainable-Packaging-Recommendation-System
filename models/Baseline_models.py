import pandas as pd
import numpy as np
import os
import sys
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --- File Paths ---
TRAIN_PATH = 'ml_train_dataset.csv'
TEST_PATH = 'ml_test_dataset.csv'
METRICS_CSV_PATH = 'ml/metrics/baseline_metrics.csv'
SUMMARY_MD_PATH = 'docs/baseline_model_summary.md'

os.makedirs('ml/metrics', exist_ok=True)
os.makedirs('docs', exist_ok=True)

# --- 1. Load Data ---
try:
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)
    print("Datasets loaded successfully.")
except FileNotFoundError:
    print(f"Error: Ensure {TRAIN_PATH} and {TEST_PATH} exist in the directory.")
    sys.exit(1)

# Formal Column Names from your Task Documents
TARGET_COST = 'Cost_Efficiency_Index'
TARGET_CO2 = 'CO2_Impact_Index'
ID_COLS = ['Material ID', 'product_id']

# Separate Features (X)
X_train = train_df.drop(columns=[TARGET_COST, TARGET_CO2] + ID_COLS, errors='ignore')
X_test = test_df.drop(columns=[TARGET_COST, TARGET_CO2] + ID_COLS, errors='ignore')

# --- 2. Define Training & Evaluation Function ---
def evaluate_baseline(model, X, y_train, y_test, model_name, display_name):
    # Perform 5-Fold Cross Validation on Training Data
    cv_results = cross_validate(model, X, y_train, cv=5, 
                                 scoring=['neg_mean_absolute_error', 'neg_root_mean_squared_error', 'r2'])
    
    # Fit on full training set to evaluate on hold-out test set
    model.fit(X, y_train)
    y_pred = model.predict(X_test)
    
    return {
        "Model": model_name,
        "Target": display_name,
        "CV_MAE": -cv_results['test_neg_mean_absolute_error'].mean(),
        "CV_RMSE": -cv_results['test_neg_root_mean_squared_error'].mean(),
        "CV_R2": cv_results['test_r2'].mean(),
        "Test_R2": r2_score(y_test, y_pred)
    }

# --- 3. Execute Baseline Training ---
results = []

print("Training Baseline Models...")

# Cost Prediction Baseline: Linear Regression
results.append(evaluate_baseline(
    LinearRegression(), 
    X_train, 
    train_df[TARGET_COST], 
    test_df[TARGET_COST], 
    "Linear Regression", 
    "Cost Efficiency"
))

# CO2 Prediction Baseline: Decision Tree
results.append(evaluate_baseline(
    DecisionTreeRegressor(random_state=42), 
    X_train, 
    train_df[TARGET_CO2], 
    test_df[TARGET_CO2], 
    "Decision Tree Regressor", 
    "CO2 Impact"
))

# --- 4. Save Deliverables ---
results_df = pd.DataFrame(results)
results_df.to_csv(METRICS_CSV_PATH, index=False)

# Generate Markdown Summary (Deliverable docs/baseline_model_summary.md)
summary_content = f"""
# Baseline Model Training Summary
Established baseline performance on {pd.Timestamp.now().strftime('%Y-%m-%d')}.

## Performance Metrics

| Model | Target | CV R2 | Test R2 | RMSE (Test) |
| :--- | :--- | :--- | :--- | :--- |
| {results[0]['Model']} | {results[0]['Target']} | {results[0]['CV_R2']:.4f} | {results[0]['Test_R2']:.4f} | {results[0]['CV_RMSE']:.4f} |
| {results[1]['Model']} | {results[1]['Target']} | {results[1]['CV_R2']:.4f} | {results[1]['Test_R2']:.4f} | {results[1]['CV_RMSE']:.4f} |

**Conclusion:** These baseline results represent the performance of simple models without hyperparameter optimization. These values serve as the minimum thresholds that the final Random Forest and XGBoost models must exceed.
"""

with open(SUMMARY_MD_PATH, 'w') as f:
    f.write(summary_content)

print(f"✅ Baseline task complete.")
print(f"Deliverables generated: \n1. {METRICS_CSV_PATH}\n2. {SUMMARY_MD_PATH}")