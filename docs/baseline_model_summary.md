# Baseline Model Summary

## Objective
The objective of this module is to establish baseline machine learning models
for evaluating the performance of product–material recommendation tasks.
These baseline models serve as reference points for comparing more advanced models.

---

## Baseline Models Used

### 1. Linear Regression (Cost Prediction)
- **Target Variable:** cost_per_kg
- **Reason for Selection:**
  Linear Regression is a simple and interpretable model.
  It provides a strong baseline for understanding linear relationships
  between integrated product–material features and cost.

---

### 2. Decision Tree Regressor (CO₂ Emission Prediction)
- **Target Variable:** co2_emission_kg_per_kg
- **Reason for Selection:**
  Decision Trees can model non-linear relationships and interactions
  between features, making them suitable as a baseline for CO₂ impact prediction.

---

## Data Used
- Integrated product–material dataset
- Compatibility rules applied before training
- Separate feature (X) and target (y) datasets created

---

## Evaluation Strategy
- Train–test split (80–20)
- 5-fold cross-validation
- Evaluation metrics:
  - Mean Absolute Error (MAE)
  - Root Mean Squared Error (RMSE)
  - R² Score
