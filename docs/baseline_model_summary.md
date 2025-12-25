# Baseline Model Training Summary

## Selected Baseline Models

### 1. Linear Regression
**Target:** Cost per Unit (USD)

**Rationale:**
- Linear Regression is simple and highly interpretable.
- Useful for understanding linear relationships between product/material features and cost.
- Serves as a strong baseline for regression tasks.

**Assumptions:**
- Linear relationship between features and target
- No strong multicollinearity
- Errors are independently distributed

**Limitations:**
- Cannot model non-linear interactions
- Sensitive to outliers

---

### 2. Decision Tree Regressor
**Target:** Carbon Footprint (kg CO₂/unit)

**Rationale:**
- Captures non-linear relationships effectively
- Handles feature interactions automatically
- Easy to visualize and interpret

**Limitations:**
- Can overfit on small or highly structured datasets
- Sensitive to small data changes

---

## Training Strategy
- Same feature set used across models where applicable
- K-Fold Cross-Validation applied for robust evaluation
- Default hyperparameters used to maintain baseline simplicity
- Strict separation of training and test datasets to avoid data leakage
