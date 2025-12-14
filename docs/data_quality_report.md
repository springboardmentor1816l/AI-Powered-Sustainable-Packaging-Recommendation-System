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
