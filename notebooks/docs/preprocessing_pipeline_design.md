
# Preprocessing Pipeline Design

## 1. Feature Groups
- **Numeric Features:** ['density', 'cost_per_kg', 'recyclability_percent', 'biodegradability_percent', 'co2_factor']
- **Categorical Features:** ['industry_use_case_enc']

## 2. Transformations Applied
- **Numeric:** Median Imputation followed by Standard Scaling (Z-score normalization).
- **Categorical:** Most Frequent Imputation followed by One-Hot Encoding.

## 3. Implementation Details
- **Tool:** Scikit-Learn `ColumnTransformer`
- **Artifact:** `preprocessing_pipeline.pkl`
- **Date:** 2025-12-19
