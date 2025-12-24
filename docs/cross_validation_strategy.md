# Cross-Validation Strategy – EcoPackAI

## Overview
This document defines the cross-validation (CV) approach used to evaluate
machine learning models in EcoPackAI. The strategy ensures robust,
unbiased performance estimation and supports reliable model comparison.

---

## Cross-Validation Method
- Technique: Stratified K-Fold Cross-Validation
- Number of Folds (K): 5

Stratification is applied to preserve the class distribution of the
primary classification target (recommended_material) across all folds.

---

## Justification
- Ensures each fold is representative of the full dataset
- Reduces variance in performance estimates
- Suitable for multi-class classification problems
- Works well with moderate-sized datasets (~400+ rows)

---

## Data Leakage Prevention
- Cross-validation is performed only on the training set
- Test set is kept completely separate as a final hold-out
- Preprocessing pipeline (imputation, scaling, encoding) is fitted
  within each fold during training
- No information from validation folds is used during fitting

---

## Reproducibility
- Fixed random_state used for fold generation
- Consistent fold splits across repeated runs
- Enables fair comparison between different models and hyperparameters

---

## Evaluation Usage
Cross-validation results are used to:
- Compare candidate models
- Tune hyperparameters
- Detect overfitting or underfitting
- Select the best performing model for final testing

---

## Conclusion
The defined cross-validation strategy provides a reliable and scalable
framework for model evaluation in EcoPackAI while maintaining strict
data isolation and reproducibility.
