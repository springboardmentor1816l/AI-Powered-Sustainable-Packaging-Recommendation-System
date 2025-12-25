# XGBoost CO₂ Prediction Model — Training Summary

## Objective
Train an XGBoost regression model to predict CO₂ emissions per unit for sustainable packaging recommendations.

## Dataset
- Integrated Product–Material dataset
- 547,874 samples
- 11 engineered input features

## Model
- Algorithm: XGBoost Regressor
- Objective: reg:squarederror
- n_estimators: 300
- max_depth: 8
- learning_rate: 0.05
- subsample: 0.8
- colsample_bytree: 0.8

## Performance
| Metric | Value |
|------|------|
| MAE | 0.004979 |
| RMSE | 0.012807 |
| R² | 0.999677 |

## Outputs
- Model: `ml/models/xgb_co2.joblib`
- Metrics: `ml/metrics/co2_metrics.csv`
- Feature Importance: `reports/feature_importance.csv`

## Notes
The XGBoost model significantly outperforms baseline models, demonstrating strong nonlinear learning capability for CO₂ emission prediction.
