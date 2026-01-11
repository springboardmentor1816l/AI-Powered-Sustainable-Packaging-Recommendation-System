# EcoPackAI — Data Quality Report (EDA)

Project: **EcoPackAI – AI-Powered Sustainable Packaging Recommendation System**  
Module: **Data Exploration & Quality Assessment (EDA)**  
Deliverable: **data_quality_report.md**

---

## 1) Datasets Used

This EDA and quality assessment was performed on the following datasets:

### Raw Datasets
- `data/raw_datasets/materials/materials_raw.csv`
- `data/raw_datasets/products/products_raw.csv`

### Processed / Cleaned Datasets
- `data/processed/materials_db.csv`
- `data/processed/products.csv`

---

## 2) Objective

The goal of this task was to:
- Understand dataset structure (rows, columns, datatypes)
- Identify missing values and inconsistencies
- Detect duplicate records
- Detect anomalies/outliers
- Generate summary statistics and visualizations
- Prepare datasets for ML pipeline and PostgreSQL ingestion

---

## 3) Structure Overview

### Materials Dataset (RAW)
- Contains packaging material properties and sustainability-related attributes
- Includes both numeric and categorical features
- Categorical columns represent use-case segments and supplier information

### Products Dataset (RAW)
- Contains product packaging attributes
- Includes product category, weight, fragility level, and shipping-related fields

---

## 4) Missing Values Analysis

Missing values were checked using:
- `df.isna().sum()`
- Missing value percentage calculated using row count

### Findings
- Some sustainability-related columns contained missing values
- Missing values were more common in optional supplier-related fields

### Output Files Generated
Missing value tables were saved to:
- `data/processed/missing_value_table_materials.csv`
- `data/processed/missing_value_table_products.csv`

---

## 5) Duplicate Records

Duplicate records were checked using:
- `df.duplicated().sum()`

### Findings
- Duplicate records were identified (if present) and flagged for removal in cleaning steps.
- Processed datasets were intended to remove duplicates where applicable.

---

## 6) Outliers & Anomaly Detection

Outliers were checked using:
- Boxplots for numerical columns
- IQR-based detection (planned for advanced cleaning)

### Findings
- Certain numeric columns showed extreme values (potential outliers)
- Outliers may be valid in real-world packaging datasets but require clipping or transformation for ML training

---

## 7) Data Consistency Checks (Rule Validation)

Rules checked / planned to be enforced:
- Percentage-based fields must remain in the range **0–100**
  - Recyclability (%)
  - Biodegradability (%)
- Cost values should not be negative
- Handling scores should fall in valid numeric ranges

---

## 8) Visualizations Created in EDA Notebook

The following plots were included in `EDA.ipynb`:
- Histograms (distribution of numeric features)
- Boxplots (outlier detection)
- Correlation heatmap (relationship between numeric features)

---

## 9) Summary of Key Issues Identified

| Issue Type | Observed |
|----------|----------|
| Missing values | ✅ Found in some columns |
| Duplicates | ✅ Checked and flagged |
| Outliers | ✅ Detected in numeric features |
| Inconsistent naming | ✅ Standardized to snake_case in cleaning |
| Range validation | ✅ Planned for % and cost columns |

---

## 10) Recommended Cleaning Actions (Next Steps)

The following cleaning actions are recommended before ML training:
1. Standardize column names (snake_case)
2. Drop duplicate rows
3. Handle missing values:
   - Numeric: mean/median imputation
   - Categorical: mode / "unknown"
4. Outlier handling:
   - IQR clipping OR log transformation for cost
5. Validate business rules and invalid values

---

## 11) Conclusion

The datasets are usable for:
- PostgreSQL ingestion and testing
- ML feature engineering
- Cost + CO₂ recommendation modelling
- Dashboard analytics

After EDA, the datasets are ready for structured cleaning, feature engineering, and ML dataset preparation.

---
