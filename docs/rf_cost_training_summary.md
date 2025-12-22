# Random Forest Cost Model – Training Summary

## Project
EcoPackAI – AI-Powered Sustainable Packaging Recommendation System

## Objective
Train a Random Forest regression model to predict **cost per unit (USD)** using integrated
product and material features.

---

## Dataset
- Source: Integrated Product–Material Dataset
- Rows: 547,874
- Features: 28
- Target Variable: `cost_per_unit_usd`

---

## Features Used
### Product Features
- product_weight_kg
- fragility_index
- shipping_type
- category

### Material Features
- material_type
- packaging_type
- recyclability_pct
- load_handling_score
- moisture_resistance_score
- thermal_resistance_score
- supplier_sustainability_compliance_pct
- sustainability_target_progress_pct

---

## Model Configuration
- Model: RandomForestRegressor
- Number of Trees: Default
- Random State: Fixed for reproducibility
- Max Depth: Default
- Criterion: Squared Error

---

## Training Strategy
- Train/Test Split: 80/20
- Cross-Validation: 5-Fold CV
- No data leakage (targets excluded from features)

---

## Evaluation Metrics
| Metric | Value |
|------|------|
MAE | 0.002904 |
RMSE | 0.028712 |
R² | 0.999984 |
CV MAE | 0.002792 |

---

## Observations
- Random Forest significantly outperforms baseline Linear Regression.
- High R² due to structured and rule-driven dataset.
- Model generalizes well across folds.

---

## Model Artifact
Saved at:
