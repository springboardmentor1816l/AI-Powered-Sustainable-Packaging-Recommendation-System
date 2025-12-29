# Baseline Model Summary

## Overview

This document summarizes the baseline models trained for the EcoPackAI project.

**Generated:** 2025-12-26 20:12:06

---

## Models Trained

### cost_per_unit_usd

**Model:** Linear Regression

**Rationale:** Simple linear model to establish baseline cost prediction

**Assumptions:** Linear relationship between features and cost

**Performance:**
- Test MAE: 0.3702
- Test RMSE: 0.4914
- Test R²: 0.9952

**Cross-Validation (5 folds):**
- CV MAE: 0.4009 ± 0.0305
- CV RMSE: 0.5180 ± 0.0238
- CV R²: 0.9945 ± 0.0008

### co2_emission_per_kg_estimated

**Model:** Decision Tree Regressor

**Rationale:** Tree-based model captures non-linear patterns in CO2 emissions

**Assumptions:** Piecewise constant approximation with depth limit

**Performance:**
- Test MAE: 0.0374
- Test RMSE: 0.0606
- Test R²: 0.9932

**Cross-Validation (5 folds):**
- CV MAE: 0.0548 ± 0.0167
- CV RMSE: 0.1299 ± 0.0881
- CV R²: 0.9518 ± 0.0566

---

## Model Configuration

- **Random Seed:** 42
- **Train/Test Split:** 80% / 20%
- **Cross-Validation Folds:** 5
- **Stratification:** By material_type

---

## Next Steps

1. Compare baseline performance with advanced models
2. Investigate feature importance
3. Identify areas for improvement
4. Tune hyperparameters if needed
