# Random Forest Cost Prediction – Training Summary

## Model
Random Forest Regressor

## Objective
Predict packaging cost per unit (INR) using integrated product and material features.

## Input Features
- Product attributes (weight, fragility, shipping type)
- Material sustainability and durability attributes

## Target Variable
Cost per unit (INR)

## Hyperparameters
- n_estimators: 200
- max_depth: 12
- random_state: 42

## Evaluation Metrics
- MAE
- RMSE
- R² Score

## Observations
Random Forest captured non-linear relationships effectively and improved over baseline linear models.
