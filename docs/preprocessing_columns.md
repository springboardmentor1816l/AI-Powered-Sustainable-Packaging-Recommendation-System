# Preprocessing Column Groups

This document defines the column groups used in the preprocessing pipeline
for the EcoPackAI project.

---

## Numeric Columns
These columns are scaled using StandardScaler after median imputation.

- product_weight
- fragility_index

---

## Categorical Columns
These columns are encoded using OneHotEncoder after most-frequent imputation.

- category
- shipping_type

---

## Excluded Columns
These columns are excluded from preprocessing as they are identifiers.

- product_id
- product_name
