# Data Quality Report

## 1. Introduction
This report summarizes the data quality assessment for the **materials** and **products** datasets used in the EcoPackAI system. The analysis includes missing values, outliers, datatype validation, and data cleaning steps performed during the EDA phase (Day 6).

---

## 2. Dataset Overview

### Materials Dataset
- 404 rows
- Contains material properties, recyclability metrics, CO2 emission scores, and sustainability attributes.
- Several columns originally contained missing numeric values.

### Products Dataset
- 404 rows
- Contains packaging types, product categories, fragility indicators, and product weights.
- Some essential columns were missing values.

---

## 3. Missing Data Analysis

### Materials Dataset – Missing Columns
- `strength_mpa`
- `weight_capacity`
- `biodegradability_percent`
- `cost_per_kg`

These fields were missing because the original dataset did not supply these attributes.  
The missing values were filled using **realistic default values** based on the material type.

### Products Dataset – Missing Columns
- `product_weight`
- `fragility_index`
- `shipping_type`

These values were filled using **default values assigned based on packaging type or name keywords**.

A missing-value summary was exported as:

# Data Quality Report — Week 9

All automated tests were executed using pytest to validate the materials and products datasets.

---

## ✔ Passed Checks
- No missing values  
- No duplicates  
- All numerical values within valid ranges  
- All categorical values valid (0/1 one-hot)  
- CII, CEI, MSS between 0–100  
- No negative or infinity values  
- All required columns present  
- All product requirement columns are valid (1–10)

---

## Final Status
Both datasets are **clean**, **validated**, and **ready for export as Parquet** and for the ML pipeline.



