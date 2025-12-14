# EcoPackAI — Data Dictionary v2
**Module:** Save Processed Dataset & Document Schema

---

## Dataset-Level Summary

- Dataset name: materials_model_ready.parquet
- Number of rows: 404
- Number of columns: 35
- Dataset type: Production-ready ML dataset

### Feature Groups
- Raw attributes
- Encoded categorical features
- Scaled numerical features
- Sustainability & performance indicators

---

## Column-Level Details

| Column Name | Data Type | Description | Range / Categories | Example | Nullable | Derived | Used in ML |
|------------|----------|-------------|--------------------|--------|----------|---------|------------|
| Material ID | string | Unique material identifier | MAT_* | MAT_0001 | No | No | Yes |
| Packaging Type | float | Ordinal encoded packaging type | ≥ 0 | 2.0 | No | Yes | Yes |
| Material Type | float | Ordinal encoded material type | ≥ 0 | 1.0 | No | Yes | Yes |
| Supplier Region | float | Ordinal encoded region | ≥ 0 | 3.0 | No | Yes | Yes |
| Recyclability (%) | float | Recyclable portion | 0–100 | 75.0 | No | No | Yes |
| Carbon Footprint (kg CO2/unit) | float | Standard-scaled footprint | ℝ | -0.84 | No | Yes | Yes |
| Cost per Unit (USD) | float | Material cost | >0 | 2.75 | No | No | Yes |
| product_cat_* | int | Product category one-hot | {0,1} | 1 | No | Yes | Yes |
| usecase_* | int | Use case one-hot | {0,1} | 0 | No | Yes | Yes |
| Recyclability Category_High | int | Binary recyclability flag | {0,1} | 1 | No | Yes | Yes |

---

## Notes
- All percentage columns constrained to 0–100
- All encoded categorical features are numeric
- Dataset validated using automated unit tests
