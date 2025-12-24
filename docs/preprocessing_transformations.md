# Preprocessing Transformations – EcoPackAI

## Overview
This document defines the preprocessing transformations applied to
each feature group using a ColumnTransformer. The transformations
ensure consistency, scalability, and prevention of data leakage
during training and inference.

---

## A. Numeric Features

### Columns
- strength_mpa
- weight_capacity
- moisture_resistance_score
- thermal_resistance_score
- biodegradability_percent
- recyclability_percent
- co2_emission_score
- cost_per_kg
- CO2_Impact_Index
- Cost_Efficiency_Index
- Material_Suitability_Score

### Transformations
1. **Missing Value Imputation**
   - Strategy: Median
   - Reason: Robust to outliers and skewed distributions

2. **Scaling**
   - Method: MinMaxScaler (0–1)
   - Reason: Ensures uniform feature scale for ML models

---

## B. Categorical Features

### Columns
- material_type
- indusrty_use_case
- recyclability_category
- packaging_type
- supplier_region

### Transformations
1. **Missing Value Handling**
   - Strategy: Replace with "Unknown"
   - Reason: Preserve row count and handle incomplete entries

2. **Encoding**
   - Method: One-Hot Encoding
   - Configuration:
     - handle_unknown = "ignore"
   - Reason: Prevent inference-time failures on unseen categories

---

## C. Binary / Boolean Features

### Columns
- hazardous_material_flag

### Transformations
1. **Type Conversion**
   - Convert True/False or Yes/No to 1/0
   - Reason: Compatibility with numerical ML models

---

## D. Excluded Columns

### Columns
- material_id
- product_id
- free_text_descriptions
- audit_fields
- target variable(s)

### Handling
- Dropped before preprocessing
- Never passed into model pipeline

---

## Consistency Guarantees
- Same preprocessing pipeline used for:
  - Training
  - Validation
  - Inference
- Scalers and encoders are fitted only on training data
- Saved pipeline artifacts reused during prediction

---

## Conclusion
The defined transformations ensure clean, standardized, and
production-ready feature inputs for EcoPackAI’s machine learning
models.
