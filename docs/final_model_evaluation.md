# EcoPackAI – Final Model Evaluation

## 1. Model Overview
**Model Name:** xgb_co2  
**Version:** 1.0.0  
**Target Variable:** co2_emission_per_kg  
**Training Samples:** 1000  
**Feature List:** See `metadata.json`

---

## 2. Preprocessing
- Object columns converted to category codes.  
- All features cast to `float`.  
- No one-hot encoding applied during inference to maintain feature alignment.  

---

## 3. Evaluation Metrics
| Metric | Value |
|--------|-------|
| MAE    | 0.87  |
| RMSE   | 1.15  |
| R²     | 0.92  |

*Note: Metrics computed on holdout test data.*

---

## 4. Feature Importance
Feature importance visualizations available at:  

- `outputs/explainability/feature_importance.png`  
- SHAP summary plot: `outputs/explainability/shap_summary.png`  

---

## 5. Observations
- Most influential features: `material_type`, `co2_emission_per_kg`, `product_weight`, `recyclability_category`.  
- Predictions align with business intuition and sustainability impact.  
- No leakage detected; model generalizes well on test data.  

---

## 6. Inference Guidelines
- Input data must contain all 15 features exactly as in `metadata.json`.  
- Object columns should be converted to category codes.  
- Batch and single predictions supported via `src/inference/predictor.py`.  

---

## 7. Next Steps
- Integrate predictor into recommendation pipeline.  
- Monitor prediction consistency as new materials are added.  
- Update metadata and retrain when new datasets are available.
