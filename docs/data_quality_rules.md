# EcoPackAI — Data Quality Rules
**Module:** Data Quality Checks & Unit Tests

## Dataset Scope
These data quality rules are applied to the processed dataset used for
machine learning and downstream analytics:

- Dataset: `materials_final_encoded.csv`

Extra columns may exist in the dataset and are allowed.
Only the required columns listed below are validated.

---

## 1. Structural Rules

### Required Columns
The dataset must contain the following columns:

- Material ID
- Packaging Type
- Material Type
- Supplier Region
- Recyclability (%)
- Recycled Content (%)
- Reusability (%)
- Biodegradation Time (days)
- End-of-Life Disposal (%)
- Carbon Footprint (kg CO2/unit)
- CO2 Emission per kg (estimated)
- Waste Reduction Impact (%)
- Sustainability Target Progress (%)
- Load Handling Score
- Moisture Resistance Score
- Thermal Resistance Score
- Cost per Unit (USD)
- Annual Usage (units)
- Total Material Weight (tons)
- Supplier Sustainability Compliance (%)
- product_cat_* (multi-label one-hot encoded)
- usecase_* (multi-label one-hot encoded)
- Recyclability Category_High
- Recyclability Category_Medium

Extra columns are ignored.

---

## 2. Missing Value Rules

- No column is allowed to contain NULL / NaN values.
- Any missing value constitutes a test failure.

---

## 3. Numeric Range Rules

The following constraints apply:

- Percentages (%) must be in the range **0–100**
- Scores must be **non-negative**
- Cost per Unit (USD) > 0
- Annual Usage (units) ≥ 0
- Total Material Weight (tons) ≥ 0
- Carbon Footprint values ≥ 0
- CO2 Emission per kg ≥ 0

---

## 4. Categorical & Encoded Feature Rules

- Encoded category columns must contain only numeric values (0/1 for one-hot)
- Recyclability Category columns must be binary
- Multi-label encoded columns must contain only 0 or 1

---

## 5. Uniqueness & Integrity Rules

- Material ID must be unique
- Duplicate rows are not allowed

---

## 6. Outcome

If all rules pass, the dataset is considered: Clean, Consistent and Safe for downstream processing