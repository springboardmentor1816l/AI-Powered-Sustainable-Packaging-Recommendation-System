# Baseline Model Training Summary
Project: EcoPackAI – AI-Powered Sustainable Packaging Recommendation System  
Module: Train Baseline Models & Compute Evaluation Metrics

## Objective
The purpose of this module is to establish simple, interpretable baseline machine learning models for predicting:
- Packaging material cost
- Environmental impact (CO₂ emission)

These baselines act as reference points for evaluating future, more complex models.

---

## Selected Baseline Models

### 1. Linear Regression
**Used for:**
- Cost per unit prediction
- CO₂ emission per kg prediction

**Rationale:**
- Simple and highly interpretable
- Assumes linear relationship between features and target
- Acts as a strong baseline for regression tasks

**Assumptions:**
- Linear relationship between features and target
- No strong multicollinearity
- Homoscedastic errors

**Limitations:**
- Cannot capture non-linear relationships
- Sensitive to outliers

---

### 2. Decision Tree Regressor
**Used for:**
- Cost per unit prediction
- CO₂ emission per kg prediction

**Rationale:**
- Captures non-linear relationships
- Handles feature interactions automatically
- Easy to visualize and explain

**Assumptions:**
- None about linearity or feature distribution

**Limitations:**
- High risk of overfitting
- Poor generalization without pruning or regularization

---

## Training Strategy
- Models were trained on the integrated product–material dataset.
- Train/test split ensured no data leakage.
- Cross-validation was applied for robust metric estimation.
- Default hyperparameters were used to maintain baseline simplicity.

---

## Conclusion
The selected baseline models provide:
- A transparent performance benchmark
- A foundation for future tuning and advanced modeling
- Clear interpretability for stakeholders and reviewers
