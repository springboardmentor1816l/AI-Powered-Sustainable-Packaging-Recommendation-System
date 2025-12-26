# XGBoost CO₂ Emission Prediction – Training Summary

## Objective
Predict CO₂ emissions per unit using combined product and material features.

## Model
XGBoost Regressor

## Inputs
- X_raw.csv
- y_co2.csv
- preprocessing_pipeline.joblib

## Hyperparameters
- objective: reg:squarederror
- n_estimators: 300
- max_depth: 6
- learning_rate: 0.05
- subsample: 0.8
- colsample_bytree: 0.8

## Evaluation Metrics
- MAE
- RMSE
- R² Score

## Observations
XGBoost effectively captures non-linear relationships between material properties, shipping method, and CO₂ emissions.
