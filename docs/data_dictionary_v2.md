# Data Dictionary v2 – EcoPackAI

## Overview
This document defines the final schema of datasets used in EcoPackAI
after data cleaning, preprocessing, feature engineering, and validation.

These datasets are used for analytics, ML training, and recommendation
pipelines.

---

## Dataset Summary

| Dataset Name | Description |
|-------------|-------------|
| materials_cleaned.parquet | Cleaned raw material dataset |
| materials_engineered.parquet | Dataset with engineered sustainability features |
| materials_model_ready.parquet | One-hot encoded and scaled ML-ready dataset |

---

## Table: materials_cleaned

| Column Name | Type | Description | Nullable | Used in ML |
|------------|------|-------------|----------|------------|
| material_id | VARCHAR | Unique material identifier | No | Yes |
| material_type | VARCHAR | Type of packaging material | No | Yes |
| strength_mpa | FLOAT | Material strength score | No | Yes |
| weight_capacity | FLOAT | Load capacity | No | Yes |
| co2_emission_score | FLOAT | CO₂ emission per kg | No | Yes |
| biodegradability_percent | FLOAT | Biodegradability percentage | No | Yes |
| recyclability_percent | FLOAT | Recyclability percentage | No | Yes |
| cost_per_kg | FLOAT | Cost per kg | No | Yes |
| indusrty_use_case | TEXT | Intended industry use | Yes | No |

---

## Engineered Features

| Column Name | Type | Description | Range | Derived |
|------------|------|-------------|-------|---------|
| CO2_Impact_Index | FLOAT | Environmental sustainability score | 0–100 | Yes |
| Cost_Efficiency_Index | FLOAT | Cost effectiveness score | 0–100 | Yes |
| Material_Suitability_Score | FLOAT | Product-material suitability score | 0–100 | Yes |

---

## Model-Ready Dataset Notes
- Categorical features are one-hot encoded
- Numerical features are MinMax scaled (0–1)
- material_id and text fields are encoded into binary columns
- Dataset contains no missing or infinite values

---

## Conclusion
This schema represents the finalized, validated data structure for
EcoPackAI’s ML and recommendation workflows.
