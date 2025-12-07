# Data Validation Report — EcoPackAI

## 1. Datasets Ingested

- `data/raw_datasets/materials.csv`
- `data/raw_datasets/products.csv`

## 2. Validation Summary

### materials.csv
- Rows: 4
- Columns: 8
- Missing values: 0 in all columns
- Duplicates: 0 (dropped if any)
- All columns in correct types:
  - strength_mpa, weight_capacity, biodegradability_percent, co2_emission_score,
    recyclability_percent, cost_per_kg → float
  - material_type, industry_use_case → text

### products.csv
- Rows: 4
- Columns: 5
- Missing values: 0 in all columns
- Duplicates: 0
- Data types:
  - product_weight → float
  - fragility_index → int
  - product_name, category, shipping_type → text

## 3. Cleaning Performed

- Dropped exact duplicate rows (if present)
- Dropped fully empty rows
- Verified column names already in snake_case and consistent with DB schema

## 4. Database Ingestion

- Inserted into PostgreSQL database: `ecopackai_db`
- Tables populated:
  - `materials` — 4 rows
  - `products` — 4 rows

## 5. Notes / Next Steps

- More real-world datasets from Kaggle/Gov portals can replace these sample CSVs.
- Same script (`scripts/ingestion/ingest_data.py`) can be reused with larger files.
