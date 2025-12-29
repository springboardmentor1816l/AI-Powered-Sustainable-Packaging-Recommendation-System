# Cross-Validation Strategy

## Overview

This document defines the cross-validation strategy for model evaluation in the EcoPackAI project.

**Strategy:** StratifiedKFold

---

## Configuration

- **Number of Folds:** 5
- **Shuffle:** True
- **Random Seed:** 42
- **Stratification:** material_type

---

## Rationale

### Why Stratified K-Fold?

1. **Maintains Class Distribution:** Each fold preserves the proportion of material types
2. **Reduces Variance:** More reliable performance estimates across folds
3. **Better Generalization:** Ensures all material types are represented in training and validation
4. **Reproducibility:** Fixed random seed allows exact fold reproduction

### Why 5 Folds?

- **Balance:** Good trade-off between bias and variance
- **Computational Efficiency:** Reasonable training time
- **Data Utilization:** Each fold uses 80% for training, 20% for validation
- **Statistical Reliability:** 5 evaluations provide robust performance estimates

---

## Fold Statistics

| Fold | Train Samples | Val Samples | Train % | Val % |
|------|---------------|-------------|---------|-------|
| 1 | 257 | 65 | 79.8% | 20.2% |
| 2 | 257 | 65 | 79.8% | 20.2% |
| 3 | 258 | 64 | 80.1% | 19.9% |
| 4 | 258 | 64 | 80.1% | 19.9% |
| 5 | 258 | 64 | 80.1% | 19.9% |

---

## Implementation

```python
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

# Prepare stratification labels
le = LabelEncoder()
stratify_labels = le.fit_transform(train_df['material_type'])

# Create cross-validator
skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# Iterate through folds
for fold_idx, (train_idx, val_idx) in enumerate(skf.split(train_df, stratify_labels), 1):
    fold_train = train_df.iloc[train_idx]
    fold_val = train_df.iloc[val_idx]
    # Train and evaluate model
    ...
```

---

## Expected Usage

This cross-validation strategy should be used for:

1. **Hyperparameter Tuning:** Finding optimal model parameters
2. **Model Selection:** Comparing different algorithms
3. **Performance Estimation:** Getting reliable metrics before final test
4. **Feature Selection:** Identifying most important features

**Important:** The test set should **never** be used during cross-validation. It is reserved for final model evaluation only.
