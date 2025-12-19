# Preprocessing Column Definitions

This document defines how input features are grouped and handled in the preprocessing pipeline for EcoPackAI.

The preprocessing pipeline is implemented using `sklearn.compose.ColumnTransformer` to ensure consistent transformations during training and inference.

---

## 🎯 Target Variable (Excluded)

The following column is **explicitly excluded** from preprocessing:

- `recommended_material`  
  - Description: Final material recommendation label
  - Used only as model target

---

## 🔢 Numeric Features

These features are continuous or ordinal numeric values and undergo:
- Median imputation for missing values
- Standard scaling (mean = 0, std = 1)

| Column Name | Description |
|------------|-------------|
| moisture_resistance_score | Resistance to moisture exposure |
| thermal_resistance_score | Resistance to thermal stress |
| Load Handling Score | Load-bearing capability score |
| CO2 Emission per kg (estimated) | Estimated carbon emission |
| Biodegradation Time (days) | Time required to biodegrade |
| Reusability (%) | Percentage reusability |
| supplier_sustainability_compliance_pct | Supplier sustainability compliance |
| Waste Reduction Impact (%) | Waste reduction contribution |
| Sustainability Target Progress (%) | Progress toward sustainability goals |
| Cost per Unit (USD) | Material cost per unit |
| Annual Usage (units) | Annual usage volume |
| Total Material Weight (tons) | Total weight consumed annually |
| CII | CO₂ Impact Index (engineered feature) |
| CEI | Cost Efficiency Index (engineered feature) |
| MSS | Material Suitability Score (engineered feature) |

---

## 🧵 Categorical Features

These features represent discrete categories and undergo:
- Most-frequent value imputation
- One-hot encoding with unknown-category handling

| Column Name | Description |
|------------|-------------|
| material_type | Base material classification |
| Recyclability Category | Recyclability level (A–D or equivalent) |

---

## ❌ Excluded Columns

The following types of columns are intentionally excluded:
- Target variables
- Free-text descriptions
- Identifiers (Product ID, Material ID)
- Audit or logging fields

---

## ✅ Notes

- All column names must match the dataset schema exactly.
- Any schema changes require updating both this document and the preprocessing pipeline.
