## Baseline Evaluation Report

### Evaluation Setup
- Cross-Validation: 5-fold GroupKFold
- Grouping Column: product_product_id
- Metrics: MAE, RMSE, R²
- Random Seed: 42 (Decision Tree)

### Key Observations
- Linear Regression provides a stable baseline for cost prediction
- Decision Tree captures non-linear patterns in CO₂ emissions
- Group-aware validation ensures no product-level leakage

### Notes
These results serve as baseline benchmarks and are not expected
to represent optimal performance.
