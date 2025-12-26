## Random Forest Cost Model — Training Summary

### Objective
Train a non-linear ensemble model to predict material cost per unit and
compare its performance against the linear baseline.

### Model Configuration
- Model: RandomForestRegressor
- n_estimators: 200
- max_depth: None
- random_state: 42
- n_jobs: -1

### Data & Preprocessing
- Input features: X_raw.csv
- Target: material_cost_per_unit_usd
- Preprocessing: Reused ColumnTransformer pipeline
- Identifiers excluded from feature space

### Evaluation
- Strategy: 5-fold GroupKFold
- Grouping: product_product_id
- Metrics: MAE, RMSE, R²

### Outcome
The Random Forest model serves as a stronger baseline capable of capturing
non-linear relationships. Performance is compared against Linear Regression
to assess marginal gains and diminishing returns.
