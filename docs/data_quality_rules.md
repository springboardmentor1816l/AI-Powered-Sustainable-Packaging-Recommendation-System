# Data Quality Rules – EcoPackAI

## Overview
This document defines the data quality rules applied to the processed
datasets used in the EcoPackAI pipeline. These rules ensure data
consistency, correctness, and reliability before model training and
deployment.

---

## 1. Mandatory Columns
The following columns must be present and must not contain null values:
- material_id
- material_type
- cost_per_kg
- co2_emission_per_kg
- recyclability_category

---

## 2. Missing Value Rules
- Mandatory columns must not contain NULL or NaN values.
- Optional columns may contain NULL values where applicable:
  - supplier_notes
  - special_handling_instructions
- Rows with missing values in mandatory columns are not allowed.

---

## 3. Value Range Rules

### Numeric Fields
- cost_per_kg > 0
- co2_emission_per_kg ≥ 0
- moisture_resistance_score between 1 and 10
- thermal_resistance_score between 1 and 10
- biodegradation_time_days ≥ 1
- recyclability_percent between 0 and 100

---

## 4. Categorical Value Rules

### Allowed Categories
- Packaging Type:
  - Box
  - Pouch
  - Tray
  - Wrap
  - Compostable Sheet

- Material Type:
  - Paper
  - Plastic
  - Metal
  - Bio-based

- Recyclability Category:
  - A
  - B
  - C
  - D

Any value outside these predefined categories is considered invalid.

---

## 5. Uniqueness & Integrity Rules
- material_id must be unique across the dataset.
- Duplicate rows are not allowed.
- Negative weights or dimensions are not permitted.

---

## 6. Normalization & Encoding Expectations
- Numeric columns must be scaled before ML training.
- Categorical columns must be encoded using approved encoding strategies.

---

## Conclusion
These data quality rules act as validation criteria for automated unit
tests and ensure only high-quality data flows into EcoPackAI’s ML and
recommendation pipelines.
