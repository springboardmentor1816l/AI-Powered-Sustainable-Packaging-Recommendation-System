# Preprocessing Column Groups – EcoPackAI

## Overview
This document defines column groupings used in the preprocessing
pipeline built with ColumnTransformer. These groups determine how
different features are transformed consistently during training
and inference.

---

## A. Numeric Features
These columns represent continuous numerical values and require
imputation and scaling.

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

Transformation:
- Missing value imputation (median)
- Scaling (MinMaxScaler)

---

## B. Categorical Features
These columns represent categories and are encoded numerically.

- material_type
- indusrty_use_case
- recyclability_category
- packaging_type
- supplier_region

Transformation:
- Missing value handling ("Unknown")
- One-Hot Encoding
- Handle unknown categories safely

---

## C. Binary / Boolean Features
These columns represent yes/no type attributes.

- hazardous_material_flag

Transformation:
- Convert to numeric binary (0 / 1)

---

## D. Excluded Columns
These columns are excluded from preprocessing and model input.

- material_id
- product_id
- free_text_descriptions
- audit_fields
- target variable(s)

---

## Notes
- Column lists are frozen to prevent schema drift.
- Any schema change requires updating this document.
