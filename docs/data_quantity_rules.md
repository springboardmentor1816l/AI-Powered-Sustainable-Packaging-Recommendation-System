# Data Quality Rules

## Mandatory Columns
- Material
- Cost/kg
- CO₂ emission

## Missing Value Rules
- Mandatory columns must not contain null values
- Optional columns may contain nulls

## Value Range Rules
- Cost/kg > 0
- CO₂ emission ≥ 0
- Moisture resistance score: 1–10
- Thermal resistance score: 1–10
- Biodegradation days ≥ 1

## Categorical Rules
Packaging Type:
- Box, Pouch, Tray, Wrap, Compostable Sheet

Material Type:
- Paper, Plastic, Metal, Bio-based

Recyclability Category:
- A, B, C, D

## Uniqueness Rules
- Material ID must be unique
- No duplicate rows allowed
