# Baseline Model Evaluation Report
Project: EcoPackAI – AI-Powered Sustainable Packaging Recommendation System  
Module: Train Baseline Models & Compute Evaluation Metrics

## Evaluation Setup
- Dataset: Integrated product–material dataset
- Targets:
  - Cost per unit (USD)
  - CO₂ emission per kg (estimated)
- Evaluation methods:
  - Cross-validation
  - Hold-out test set

---

## Evaluation Metrics Used
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score
- Cross-validation MAE (average)

These metrics provide insight into both prediction accuracy and error distribution.

---

## Results Summary

### Linear Regression
**Observations:**
- Strong overall performance
- High R² values indicate effective linear modeling
- Errors are consistent and stable across folds

**Strengths:**
- Generalizes well
- Low variance
- Easy to interpret

**Weaknesses:**
- Limited ability to model non-linear effects

---

### Decision Tree Regressor
**Observations:**
- Extremely high R² scores
- Very low MAE and RMSE values

**Strengths:**
- Captures complex, non-linear relationships
- Fits training data very closely

**Weaknesses:**
- High risk of overfitting
- Likely memorization rather than true generalization

---

## Cross-Target Comparison
- Cost prediction and CO₂ prediction show similar trends.
- Decision Trees outperform Linear Regression numerically, but with overfitting risk.
- Linear Regression serves as a safer and more reliable baseline.

---

## Key Insights
- Baseline performance is strong due to high-quality engineered features.
- Overfitting in Decision Trees highlights the need for regularization or ensemble methods.
- These baselines provide a solid reference for future model improvements.

---

## Conclusion
The evaluation confirms that:
- Baseline models are effective and correctly implemented
- Metrics are reliable and reproducible
- Future work should focus on model regularization and advanced algorithms
