# Preprocessing Pipeline Design

This document explains the design decisions behind the preprocessing
pipeline used in the EcoPackAI system.

---

## Objective
To ensure consistent, reusable, and production-ready preprocessing
for all downstream machine learning models.

---

## Numeric Feature Processing
- Missing values are handled using median imputation.
- Features are standardized using StandardScaler.
- This ensures numeric features are on comparable scales.

---

## Categorical Feature Processing
- Missing values are handled using most-frequent imputation.
- OneHotEncoder is used to convert categories into numeric format.
- Unknown categories are ignored during inference.

---

## ColumnTransformer Usage
A ColumnTransformer is used to apply different preprocessing steps
to numeric and categorical columns simultaneously.

---

## Reusability
The preprocessing pipeline is saved as a serialized object (`.pkl`)
to ensure identical preprocessing during training and inference.
