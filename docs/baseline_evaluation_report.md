# Baseline Model Evaluation Report

## Overview
This report summarizes the performance of baseline machine learning models
trained on the integrated product–material dataset.

Baseline models are intended to provide reference performance levels
for comparison with advanced models developed later in the project.

---

## Evaluation Metrics
The following metrics were used:

- **MAE (Mean Absolute Error):**
  Measures the average magnitude of prediction errors.

- **RMSE (Root Mean Squared Error):**
  Penalizes larger prediction errors more strongly.

- **R² Score:**
  Indicates how much variance in the target variable is explained by the model.

---

## Results Summary

### Cost Prediction (Linear Regression)
- Achieved reasonable performance as a baseline.
- Captures general trends between product–material features and cost.
- Serves as a reference for more complex models.

---

### CO₂ Emission Prediction (Decision Tree)
- Captures non-linear patterns in sustainability-related features.
- Performance varies across folds, as expected for tree-based models.

---

## Cross-Validation Results
- 5-fold cross-validation confirms model stability.
- Mean R² scores provide a reliable estimate of generalization performance.
- Standard deviation values indicate acceptable variability.

---

## Conclusion
Baseline models establish a solid foundation for evaluation.
Advanced models (e.g., Random Forest) are expected to outperform
these baselines and justify increased complexity.

These results satisfy the evaluation requirements defined in the Dec 18 module.
