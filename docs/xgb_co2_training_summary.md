## XGBoost CO₂ Model — Training Summary

### Objective
Train an XGBoost regressor to predict CO₂ emission per kg and evaluate
performance using a single 80/20 train–test split.

### Target
- Column: co2_emission_per_kg_estimated

### Model Configuration
- objective: reg:squarederror
- n_estimators: 200
- max_depth: 6
- learning_rate: 0.1
- subsample: 0.8
- colsample_bytree: 0.8
- random_state: 42

### Data & Preprocessing
- Features: X_raw.csv
- Preprocessing: Reused ColumnTransformer pipeline
- Identifiers excluded from feature space

### Evaluation
- Strategy: 80/20 train–test split
- Metrics: MAE, RMSE, R²

### Notes
Given strong deterministic structure in the dataset, near-perfect
performance is expected. Results are used to support downstream
recommendation and explainability modules.
