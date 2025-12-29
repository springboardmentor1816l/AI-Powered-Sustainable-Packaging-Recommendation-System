# Baseline Model Evaluation Report

## Overview

This report provides a detailed analysis of baseline model performance for the EcoPackAI sustainable packaging recommendation system.

**Generated:** 2025-12-26 20:12:06

---

## Dataset Statistics

- **Training Samples:** 322
- **Test Samples:** 81
- **Total Samples:** 403

### Target Variable Statistics

#### cost_per_unit_usd

| Statistic | Training | Test |
|-----------|----------|------|
| Mean | 8.8369 | 9.3295 |
| Median | 3.8700 | 11.5500 |
| Std Dev | 7.0975 | 7.1050 |
| Min | 0.2100 | 1.3300 |
| Max | 25.6800 | 25.9500 |

#### co2_emission_per_kg_estimated

| Statistic | Training | Test |
|-----------|----------|------|
| Mean | 1.1447 | 1.1631 |
| Median | 1.4000 | 1.4200 |
| Std Dev | 0.7173 | 0.7377 |
| Min | 0.2800 | 0.2800 |
| Max | 3.2500 | 3.2000 |

---

## Model Performance Comparison

| Target | Model | Test MAE | Test RMSE | Test R² | CV R² |
|--------|-------|----------|-----------|---------|-------|
| cost_per_unit_usd | Linear Regression | 0.3702 | 0.4914 | 0.9952 | 0.9945 |
| co2_emission_per_kg_estimated | Decision Tree Regressor | 0.0374 | 0.0606 | 0.9932 | 0.9518 |

---

## Key Findings

### cost_per_unit_usd

**Model:** Linear Regression

**Performance Assessment:** Good

- The model explains 99.5% of the variance in cost_per_unit_usd
- ✓ Good generalization to test data
- ✓ Consistent performance across folds (σ = 0.0008)

### co2_emission_per_kg_estimated

**Model:** Decision Tree Regressor

**Performance Assessment:** Good

- The model explains 99.3% of the variance in co2_emission_per_kg_estimated
- ✓ Good generalization to test data
- ⚠️ Variable performance across folds (σ = 0.0566)

---

## Recommendations

1. **Feature Engineering:** Investigate engineered features to improve predictions
2. **Advanced Models:** Test ensemble methods (Random Forest, Gradient Boosting)
3. **Hyperparameter Tuning:** Optimize model parameters for better performance
4. **Feature Selection:** Identify and retain most important features
5. **Error Analysis:** Examine residuals to understand model limitations

---

## Conclusion

These baseline models provide a starting point for cost and CO₂ prediction. The metrics established here will serve as benchmarks for evaluating more sophisticated models and optimization strategies.
