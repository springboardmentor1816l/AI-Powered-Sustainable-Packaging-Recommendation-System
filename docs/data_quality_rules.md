
# EcoPackAI Data Quality Checklist & Rules

This document outlines the mandatory data quality rules and constraints applied to the final, engineered dataset.

## 1. Missing Value Rules
- **No Nulls in Required Fields:** Columns including Material ID, Cost per Unit (USD), and CO2 Emission per kg (estimated) **must not contain NaN/Null values.** (Handled by Median Imputation).
- **Allowed Nulls:** No fields should contain nulls in the final ML-ready dataset.

## 2. Value Range Rules
- **Positive Values:** The following scaled features must be $\geq 0.0$:
    - Cost per Unit (USD)
    - CO2 Emission per kg (estimated)
    - Biodegradation Time (days)
- **Score Range:** Moisture and Thermal resistance scores must be logically valid (Original: 1–10). In the final scaled data, this means $\geq 0.0$.

## 3. Categorical Rules
- **Valid Categories:** All One-Hot Encoded (OHE) features must contain only **0 or 1** (binary).

## 4. Uniqueness & Integrity Rules
- **Uniqueness Check:** The `Material ID` column must be unique.
- **No Duplicates:** No duplicate rows are allowed.
- **No Invalid Values:** No negative weights/dimensions or infinity values are allowed.

## 5. Feature Engineering Rules
- **Index Range:** All engineered feature columns (CO2_Impact_Index, Cost_Efficiency_Index, Material_Suitability_Score) must fall within the final **[0.0, 1.0]** scaled range.
- **Integrity:** Ensure no engineered feature produces **Infinity** or **NaN** values.
