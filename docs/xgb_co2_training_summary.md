# XGBoost CO₂ Emission Prediction - Training Summary

## Overview

This document summarizes the XGBoost model trained for CO₂ emission prediction.

**Generated:** 2025-12-26 21:22:01
**Model Type:** XGBoost Regressor
**Target:** co2_emission_per_kg_estimated (kg CO₂ per kg material)

---

## Model Configuration

### Hyperparameters

- **Objective:** reg:squarederror
- **Number of Estimators:** 200
- **Max Depth:** 6
- **Learning Rate:** 0.1
- **Subsample:** 0.8
- **Column Subsample:** 0.8
- **L1 Regularization (alpha):** 0.1
- **L2 Regularization (lambda):** 1.0
- **Random Seed:** 42

### Training Configuration

- **Training Samples:** 322
- **Test Samples:** 81
- **Features:** 17
- **Cross-Validation Folds:** 5

---

## Performance Metrics

### Test Set Performance

- **MAE:** 0.038867 kg CO₂/kg
- **RMSE:** 0.058772 kg CO₂/kg
- **R² Score:** 0.993573 (99.36% variance explained)

### Cross-Validation Performance

- **CV MAE:** 0.040784 ± 0.003495 kg CO₂/kg
- **CV RMSE:** 0.059361 ± 0.004491 kg CO₂/kg
- **CV R²:** 0.992949 ± 0.001244

---

## Comparison with Baseline

| Metric | Baseline (Decision Tree) | XGBoost | Improvement |
|--------|--------------------------|---------|-------------|
| R² | 0.993200 | 0.993573 | +0.000373 (+0.04%) |
| MAE | 0.037400 | 0.038867 | -0.001467 (-3.92%) |
| RMSE | 0.060600 | 0.058772 | +0.001828 (+3.02%) |

### Assessment

✅ **XGBoost improves upon baseline** (2/3 metrics)

---

## Model Artifacts

- **Model File:** `ml/models/xgb_co2.joblib`
- **Metrics File:** `ml/metrics/co2_metrics.csv`
- **Feature Importance:** `ml/reports/feature_importance.csv`
- **Format:** joblib (scikit-learn compatible)

### Loading the Model

```python
import joblib

# Load model
model = joblib.load('ml/models/xgb_co2.joblib')

# Make predictions
predictions = model.predict(X_new)
```

---

## Acceptance Criteria

- ✅ Model trains without errors
- ✅ RMSE: 0.058772 kg CO₂/kg
- ✅ Model file saved successfully
- ✅ Metrics logged and reproducible
- ✅ Feature importance generated

---

## Next Steps

1. Analyze feature importance in detail
2. Perform error analysis on predictions
3. Consider hyperparameter tuning if needed
4. Deploy model to inference pipeline
