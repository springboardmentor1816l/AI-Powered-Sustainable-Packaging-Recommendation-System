# Random Forest Cost Prediction - Training Summary

## Overview

This document summarizes the Random Forest model trained for packaging cost prediction.

**Generated:** 2025-12-26 21:10:18
**Model Type:** Random Forest Regressor
**Target:** cost_per_unit_usd (USD per unit)

---

## Model Configuration

### Hyperparameters

- **Number of Trees:** 100
- **Max Depth:** 15
- **Min Samples Split:** 5
- **Min Samples Leaf:** 2
- **Max Features:** sqrt
- **Random Seed:** 42

### Training Configuration

- **Training Samples:** 322
- **Test Samples:** 81
- **Features:** 18
- **Cross-Validation Folds:** 5

---

## Performance Metrics

### Test Set Performance

- **MAE:** $0.2250
- **RMSE:** $0.3809
- **R² Score:** 0.997091 (99.71% variance explained)

### Cross-Validation Performance

- **CV MAE:** $0.2874 ± $0.0169
- **CV RMSE:** $0.4306 ± $0.0402
- **CV R²:** 0.996215 ± 0.000633

---

## Comparison with Baseline

| Metric | Baseline (Linear Regression) | Random Forest | Improvement |
|--------|------------------------------|---------------|-------------|
| R² | 0.995200 | 0.997091 | +0.001891 (+0.19%) |
| MAE | $0.3702 | $0.2250 | $+0.1452 (+39.21%) |
| RMSE | $0.4914 | $0.3809 | $+0.1105 (+22.50%) |

### Assessment

✅ **Random Forest improves upon baseline** (3/3 metrics)

---

## Feature Information

**Total Features:** 18

**Feature List:**
1. `packaging_type`
2. `material_type`
3. `supplier_region`
4. `recyclability_percent`
5. `recyclability_category`
6. `recycled_content_percent`
7. `reusability_percent`
8. `biodegradation_time_days`
9. `end_of_life_disposal_percent`
10. `carbon_footprint_kg_co2_unit`
11. `waste_reduction_impact_percent`
12. `sustainability_target_progress_percent`
13. `load_handling_score`
14. `moisture_resistance_score`
15. `thermal_resistance_score`
16. `annual_usage_units`
17. `total_material_weight_tons`
18. `supplier_sustainability_compliance_percent`

---

## Model Artifacts

- **Model File:** `ml/models/rf_cost.joblib`
- **Metrics File:** `ml/metrics/rf_cost_metrics.csv`
- **Format:** joblib (scikit-learn compatible)

### Loading the Model

```python
import joblib

# Load model
model = joblib.load('ml/models/rf_cost.joblib')

# Make predictions
predictions = model.predict(X_new)
```

---

## Validation Checklist

- ✅ Random Forest model trained successfully
- ✅ Cost prediction metrics computed and reviewed
- ✅ Model performance documented
- ✅ Model artifact saved correctly
- ✅ Training details documented

---

## Next Steps

1. Analyze feature importance
2. Perform error analysis on predictions
3. Consider hyperparameter tuning if needed
4. Deploy model to backend inference pipeline
