# Data Quality Rules – EcoPackAI

Source dataset: `data/processed/cleaned_dataset.csv`

## 1. Required (mandatory) columns
These columns must exist and must not contain nulls:
- Material ID
- Material Type
- Cost per Unit (USD)
- CO2 Emission per kg (estimated)
- Biodegradation Time (days)

## 2. Allowed optional columns (nulls allowed)
- Packaging Type
- Suitable Product Categories
- Recommended Packaging Use Cases
- Supplier Region
- Recyclability (%)
- Recyclability Category
- Recycled Content (%)
- Reusability (%)
- End-of-Life Disposal (%)
- Carbon Footprint (kg CO2/unit)
- Waste Reduction Impact (%)
- Sustainability Target Progress (%)
- Load Handling Score
- Moisture Resistance Score
- Thermal Resistance Score
- Annual Usage (units)
- Total Material Weight (tons)
- Supplier Sustainability Compliance (%)

## 3. Value / Range rules (numeric)
- Cost per Unit (USD) > 0
- CO2 Emission per kg (estimated) ≥ 0
- Carbon Footprint (kg CO2/unit) ≥ 0
- Biodegradation Time (days) ≥ 1
- Recyclability (%) between 0 and 100 inclusive
- Recycled Content (%) between 0 and 100 inclusive
- Reusability (%) between 0 and 100 inclusive
- End-of-Life Disposal (%) between 0 and 100 inclusive
- Waste Reduction Impact (%) between 0 and 100 inclusive
- Sustainability Target Progress (%) between 0 and 100 inclusive
- Load Handling Score between 1 and 10 inclusive
- Moisture Resistance Score between 1 and 10 inclusive
- Thermal Resistance Score between 1 and 10 inclusive
- Annual Usage (units) ≥ 0
- Total Material Weight (tons) ≥ 0
- Supplier Sustainability Compliance (%) between 0 and 100 inclusive

## 4. Categorical rules
- Material Type must belong to: `["Paper", "Plastic", "Metal", "Bio-based"]`
- Recyclability Category must belong to: `["A", "B", "C", "D"]`

> Notes: If your project uses extra Material Types or Recyclability categories, update this list.

## 5. Uniqueness & integrity
- `Material ID` must be unique (no duplicates).
- No identical duplicate rows in the dataset.

## 6. Engineered features (when present)
- CO2_Impact_Index, Cost_Efficiency_Index, Material_Suitability_Score — each must be numeric and between 0 and 100 inclusive.

## 7. Action on failure
- Tests fail → fix the source (cleaning script), re-run cleaning, re-run tests.
- Document any tolerated exceptions in `/docs/data_quality_report.md`.
