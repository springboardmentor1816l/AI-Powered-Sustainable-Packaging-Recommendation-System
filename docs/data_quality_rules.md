# Data Quality Rules – Materials Dataset

## 1. Mandatory Columns (No Nulls Allowed)
- material_id
- material_name
- material_type
- packaging_type
- cost_per_kg
- co2_emission_per_kg
- recyclability_category

## 2. Optional Columns (Nulls Allowed)
- supplier_notes
- special_handling

## 3. Numeric Value Rules
- cost_per_kg > 0
- co2_emission_per_kg ≥ 0
- moisture_resistance_score: 1–10
- thermal_resistance_score: 1–10
- biodegradation_days ≥ 1
- No negative weights or dimensions

## 4. Categorical Rules
### Packaging Type
- Box
- Pouch
- Tray
- Wrap
- Compostable Sheet

### Material Type
- Paper
- Plastic
- Metal
- Bio-based

### Recyclability Category
- A
- B
- C
- D

## 5. Uniqueness & Integrity
- material_id must be unique
- No duplicate rows allowed

## 6. Feature Engineering Constraints
- CII, CEI, MSS scores must be between 0 and 100
- No infinite or NaN values after feature engineering
