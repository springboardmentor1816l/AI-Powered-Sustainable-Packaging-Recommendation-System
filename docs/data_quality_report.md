# EcoPackAI — Data Quality Report (Initial Exploration)

## Datasets Reviewed
- material_dataset_raw.csv
- product_dataset_raw.csv

## Identified Issues
- Inconsistent column naming conventions
- Mixed data types in numeric columns
- Missing values in raw data
- Categorical inconsistencies (case, separators)

## Outliers
- Cost, CO₂ emission score, and strength show outliers
- Values remain within realistic industrial bounds

## Duplicates
- No exact duplicate records found

## Recommendations
- Normalize column names
- Convert numeric fields to floats
- Standardize categorical values
- Apply imputation strategies (median/mode)
- Add DB constraints post-ingestion

These recommendations were implemented in subsequent cleaning steps.

**Module:** Data Quality Checks & Unit Tests

## Dataset Evaluated
- `materials_final_encoded.csv`

---

## Test Summary

| Category | Status |
|--------|--------|
| Structural checks | Passed |
| Missing value checks | Passed |
| Numeric range checks | Passed |
| Encoded feature validation | Passed |
| Uniqueness & integrity checks | Passed |

---

## Observations
- All required columns are present
- No missing values detected
- Numeric and percentage values fall within valid ranges
- Encoded categorical features contain valid binary values
- Material IDs are unique
- No duplicate records found

---

## Conclusion
The dataset satisfies all defined data quality rules and is considered
safe for downstream feature engineering, modeling, and deployment.
