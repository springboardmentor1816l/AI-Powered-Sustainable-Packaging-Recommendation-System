# Preprocessing Pipeline Design

Project: EcoPackAI  
Module: Data Preparation & ML Readiness  
Tooling: scikit-learn ColumnTransformer  

---

## 1. Overview

The preprocessing pipeline converts the raw integrated Product–Material dataset into a numerical, model-ready format.
It ensures that **training and inference use identical transformations**, preventing data leakage and inconsistency.

The pipeline is implemented using **scikit-learn's ColumnTransformer** and saved as a reusable artifact.

---

## 2. Pipeline Architecture

The preprocessing pipeline consists of three major stages:

1. Numeric feature processing
2. Categorical feature processing
3. Feature concatenation into a single numeric matrix

---

## 3. Numeric Feature Processing

### Input
Continuous and ordinal numeric columns such as cost, sustainability scores, and resistance metrics.

### Transformations Applied
1. **Missing Value Imputation**
   - Strategy: Median
   - Reason: Robust to outliers

2. **Feature Scaling**
   - Method: StandardScaler
   - Reason: Ensures comparable scale across features for ML algorithms

### Output
All numeric features transformed into standardized numerical values.

---

## 4. Categorical Feature Processing

### Input
Nominal and ordinal categorical columns such as material type and supplier region.

### Transformations Applied
1. **Missing Value Imputation**
   - Strategy: Most Frequent
   - Fallback category: "Unknown"

2. **Encoding**
   - Method: One-Hot Encoding
   - Configuration:
     - `handle_unknown="ignore"`
     - Prevents inference-time crashes

### Output
Binary encoded columns representing categorical values.

---

## 5. Excluded Columns

The following columns are intentionally excluded from preprocessing:
- Identifiers (IDs)
- Free-text descriptive fields
- Target variables
- Audit and logging metadata

This prevents target leakage and noise in model training.

---

## 6. Pipeline Fitting Strategy

- The preprocessing pipeline is fitted **only on training data**
- Learned parameters (scalers, encoders) are saved
- The same pipeline is reused for:
  - Validation
  - Testing
  - Production inference

---

## 7. Output Artifacts

| Artifact | Description |
|-------|------------|
| preprocessing_pipeline.pkl | Serialized ColumnTransformer |
| X_transformed_sample.csv | Sample transformed dataset |
| preprocessing_columns.md | Column mapping reference |

---

## 8. Benefits

- Reproducible ML experiments
- Safe deployment in APIs
- Modular and maintainable design
- Scalable to new features and datasets

---

## 9. Future Enhancements

- Feature selection integration
- Automated schema validation
- Drift detection support
