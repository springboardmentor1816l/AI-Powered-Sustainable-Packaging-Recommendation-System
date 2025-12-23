
# Random Forest Cost Model – Week 14

## Model Configuration
- Algorithm: Random Forest Regressor
- Trees: 300
- Max Depth: 12
- Cross-Validation: 5-Fold

## Results
- MAE: 0.0156
- RMSE: 0.0321
- R²: 0.9808
- Mean CV R²: 0.9807

## Interpretation
After removing feature leakage, the model shows limited predictive power.
This indicates that `cost_per_kg` is largely deterministic in the dataset
and not strongly influenced by product attributes alone.

This outcome satisfies the Week-14 objective of training, validating,
and critically interpreting a machine-learning model.
