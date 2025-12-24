
# Random Forest Cost Prediction Model – Training Summary

## Dataset
- Source: integrated_ecopack_dataset.csv
- Records: 1500000

## Target Variable
- cost_per_unit = material_cost_per_kg × product_weight
- Unit: INR per product unit

## Features Used
['product_weight', 'fragility_score', 'moisture_sensitivity', 'thermal_sensitivity', 'expected_shelf_life_days', 'biodegradability_percent', 'load_handling_score', 'co2_impact_index', 'cost_efficiency_index', 'sustainability_score', 'hazardous_material_flag']

## Model
- RandomForestRegressor
- Trees: 300
- Max Depth: 12
- Min Samples Split: 5
- Min Samples Leaf: 2

## Cross Validation
- 5-Fold CV MAE: 0.0100

## Test Metrics
- MAE: 0.0107
- RMSE: 1.1052
- R² Score: 0.9999

## Output Artifacts
- Model: ml/models/rf_cost.joblib
- Metrics: ml/metrics/rf_cost_metrics.csv
