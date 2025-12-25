# Baseline Model Evaluation Report

## Evaluation Metrics
Models were evaluated using:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

Metrics were computed using:
- Cross-validation folds
- Independent hold-out test dataset

---

## Results Summary

### Linear Regression – Cost Prediction

| Metric | Cross-Validation | Test Set |
|------|-----------------|----------|
| MAE  | 0.01545 | 0.01549 |
| RMSE | 0.14476 | 0.02101 |
| R²   | — | 0.9943 |

**Interpretation:**
- Very low MAE indicates accurate cost prediction
- High R² (≈ 0.99) shows strong explanatory power
- Slight RMSE reduction on test data suggests good generalization

---

### Decision Tree Regressor – Carbon Footprint Prediction

| Metric | Cross-Validation | Test Set |
|------|-----------------|----------|
| MAE  | ~0 | ~0 |
| RMSE | ~0 | ~0 |
| R²   | — | 1.00 |

**Interpretation:**
- Near-perfect prediction performance
- Indicates strong alignment between features and CO₂ output
- Possible risk of overfitting due to highly structured data

---

## Key Observations
- Linear Regression performs exceptionally well for cost estimation
- Decision Tree achieves near-perfect accuracy for CO₂ prediction
- Dataset appears clean, consistent, and highly informative

---
