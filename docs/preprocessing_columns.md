# Preprocessing Columns Definition

Project: EcoPackAI  
Module: Data Preparation & ML Readiness  
Artifact: ColumnTransformer Column Mapping  

---

## 1. Numeric Features

These columns contain continuous or ordinal numeric values.
They are imputed using **median strategy** and scaled using **StandardScaler**.

| Column Name |
|------------|
| product_weight_kg |
| fragility_index |
| Recyclability (%) |
| Recycled Content (%) |
| Reusability (%) |
| Biodegradation Time (days) |
| CO2 Emission per kg (estimated) |
| Waste Reduction Impact (%) |
| Supplier Sustainability Compliance (%) |
| Load Handling Score |
| Moisture Resistance Score |
| Thermal Resistance Score |

---

## 2. Categorical Features

These columns contain nominal or ordinal categorical values.
They are imputed using **most frequent value** and encoded using **OneHotEncoder**.

| Column Name |
|------------|
| shipping_type |
| category |
| Material Type |
| Packaging Type |
| Recyclability Category |
| Supplier Region |

---

## 3. Excluded Columns

These columns are **not included** in preprocessing to avoid data leakage or noise.

| Column Name | Reason |
|------------|-------|
| Material ID | Identifier |
| product_id | Identifier |
| product_name | Free-text |
| Recommended Packaging Use Cases | Free-text |
| Target Variables | Prediction targets |
| Audit / Logging fields | Non-ML fields |

---

## 4. Notes

- Column names must exactly match the integrated dataset schema
- Any schema change must be reflected here before retraining
- This document acts as the **single source of truth** for preprocessing
