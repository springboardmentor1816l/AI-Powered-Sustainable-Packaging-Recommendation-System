## Model Version History

### v1 — Baseline Models

#### cost_linear_v1_run1
- Target: Cost per unit (USD)
- Model: Linear Regression
- Dataset: v1
- Features: v1
- Evaluation: 5-fold GroupKFold
- Notes: Baseline reference model

#### co2_decision_tree_v1_run1
- Target: CO₂ emission per kg (estimated)
- Model: Decision Tree Regressor
- Dataset: v1
- Features: v1
- Evaluation: 5-fold GroupKFold
- Notes: Baseline reference model

### cost_random_forest_v1_run1
- Target: Cost per unit (USD)
- Model: RandomForestRegressor
- Dataset: v1
- Features: v1
- Evaluation: 5-fold GroupKFold
- Notes: Non-linear ensemble baseline for cost prediction

### co2_xgboost_v1_run1
- Target: CO₂ emission per kg (estimated)
- Model: XGBoost Regressor
- Dataset: v1
- Features: v1
- Evaluation: 80/20 Train–Test split
- Notes: Used for feature importance and downstream explainability