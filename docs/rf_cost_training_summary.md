
# Random Forest Cost Model — Training Summary

## Model
RandomForestRegressor

## Hyperparameters
- n_estimators: 200
- max_depth: None
- min_samples_split: 2
- min_samples_leaf: 1
- random_state: 42

## Target
- sustainability_score (Cost per unit, INR)

## Evaluation Metrics

### Cross-Validation (5-fold)
- MAE: 1.004
- RMSE: 2.989
- R²: 0.980

### Test Set
- MAE: 0.944
- RMSE: 1.737
- R²: 0.992

## Notes
- Compared against baseline models from previous module.
- Observed improvements and limitations should guide future tuning.
