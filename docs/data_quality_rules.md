# Data Quality Rules – EcoPackAI

## 1. Mandatory Columns (Must NOT be NULL)
- Cost per Unit (USD)
- CO2 Emission per kg (estimated)
- Biodegradation Time (days)
- moisture_resistance_score
- thermal_resistance_score

## 2. Numeric Value Constraints
- Cost per Unit (USD) > 0
- CO2 Emission per kg (estimated) ≥ 0
- Biodegradation Time (days) ≥ 1
- moisture_resistance_score ∈ [1, 10]
- thermal_resistance_score ∈ [1, 10]

## 3. Percentage-Based Columns
(All must be between 0 and 100)
- Reusability (%)
- End-of-Life Disposal (%)
- Waste Reduction Impact (%)
- Sustainability Target Progress (%)
- supplier_sustainability_compliance_pct

## 4. Structural Rules
- Dataset must not be empty
- No duplicate rows allowed
- All expected columns must exist

## 5. Data Integrity Rules
- No infinite values
- No NaN values in mandatory fields
- Numeric columns must be valid numeric types

## 6. ML Safety Rules
- No feature used for ML should contain NaN or infinite values
