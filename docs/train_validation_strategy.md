# Train–Validation Split Strategy – EcoPackAI

## Overview
This document describes the strategy used to split the dataset into
training and validation sets for machine learning model development
in EcoPackAI.

The goal is to ensure fair evaluation, prevent data leakage, and
maintain representative distributions across datasets.

---

## Dataset Used
- Source: materials_model_ready.parquet
- Type: One-hot encoded and scaled dataset
- Rows: ~400+
- Features: Numeric, categorical (encoded), engineered features

---

## Split Strategy

### Primary Approach
- Train–Validation split ratio: 80% / 20%
- Splitting performed after:
  - Data cleaning
  - Feature engineering
  - Encoding and scaling

---

## Stratification Strategy

### For Classification Targets
- Stratified split based on:
  - recommended_material
- Ensures balanced class distribution in both train and validation sets

---

## Randomization
- Fixed random_state used
- Ensures reproducibility of results across runs

---

## Data Leakage Prevention
- Feature scaling performed before split using fitted scaler
- No target variables included in feature set
- Engineered features derived only from input features
- Validation data never seen during training

---

## Validation Purpose
- Measure generalization performance
- Detect overfitting
- Support hyperparameter tuning

---

## Future Extension
- Cross-validation can be applied for model comparison
- Time-based split can be introduced if temporal data is added

---

## Conclusion
The defined train–validation split strategy ensures robust, reproducible,
and unbiased model evaluation for EcoPackAI.
