# EcoPackAI — Missing Value Handling Report
**Module:** Data Cleaning & Preprocessing

## 1. Objective
The objective of this task is to clean the integrated materials dataset by
identifying and handling missing, null, or corrupted values to ensure the
dataset is consistent, reliable, and ready for downstream machine learning
tasks.

This report documents the missing value analysis and cleaning decisions by
comparing:
- Input (raw dataset): `integrated_materials_dataset.csv`
- Output (cleaned dataset): `cleaned_integrated_materials.csv`

---

## 2. Dataset Overview

| Dataset | Description |
|-------|-------------|
| integrated_materials_dataset.csv | Raw integrated dataset containing material, sustainability, and supplier-related attributes |
| cleaned_integrated_materials.csv | Cleaned dataset with missing values handled and ready for preprocessing |

---

## 3. Missing Value Identification (Input Dataset)

Missing value inspection was performed using:
- `df.isnull().sum()`
- `df.info()`

### Columns observed with missing values:
- **Biodegradation Time (days)**
- **Recyclability %**
- **Waste Reduction Impact %**
- **Carbon Footprint**
- **Supplier Region**
- **Suitable Product Categories**

---

## 4. Missing Value Handling Strategy

The following strategies were applied to handle missing values:

| Column Type | Strategy Applied | Justification |
|-----------|-----------------|---------------|
| Numeric (continuous) | Median imputation | Robust to outliers and preserves central tendency |
| Numeric (percentage / impact scores) | Median imputation | Maintains scale consistency |
| Categorical | Most frequent value (mode) | Preserves dominant category |
| Critical missing rows | Row removal (if applicable) | Prevents unreliable multi-null records |

All decisions follow the recommended strategies defined in the task document.

---

## 5. Cleaning Actions Applied

- Numeric columns with missing values were imputed using **median values**
- Categorical columns were imputed using **most frequent values**
- Rows with excessive missing information (multiple critical fields missing)
  were removed where necessary
- No new missing values were introduced during cleaning

---

## 6. Post-Cleaning Validation (Output Dataset)

Validation checks on `cleaned_integrated_materials.csv` confirm:

- No remaining missing values:
`df.isnull().sum() == 0`
- All columns have valid data types
- Dataset is consistent and complete


---

## 7. Summary

- Missing values were identified in the raw integrated dataset
- Appropriate imputation and removal strategies were applied
- The cleaned dataset satisfies all validation criteria
- The output file is ready for feature encoding and normalization

**Final Output:**  
`/data/processed/cleaned_integrated_materials.csv`

---

## 8. Compliance Checklist

- [x] Raw dataset inspected  
- [x] Missing values identified  
- [x] Appropriate strategies applied  
- [x] Cleaned dataset exported  
- [x] Missing value report documented  
