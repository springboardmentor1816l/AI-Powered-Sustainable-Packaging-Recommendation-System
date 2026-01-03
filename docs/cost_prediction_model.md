# Cost Prediction Model – Random Forest

## Objective
Predict packaging material cost per kg using engineered sustainability features.

## Model
- Algorithm: RandomForestRegressor
- Version: v1
- Number of Trees: 200
- Random State: 42

## Dataset
- Source: materials_model_ready.parquet
- Target Variable: cost_per_kg

## Evaluation Metrics
- Mean Squared Error (MSE): <filled automatically>
- R² Score: <filled automatically>

## Model Artifacts
- Saved at: ml/models/cost_prediction/v1/cost_model.pkl
- Metrics logged in: ml/metrics/cost_prediction_metrics.csv
