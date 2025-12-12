# Data Quality Rules — EcoPackAI

## Mandatory columns
- MaterialID (unique), Material, Cost_per_kg, CO2_per_kg

## Missing value rules
- No nulls in mandatory fields
- Optional: Supplier Notes, Special Handling

## Value ranges
- Cost_per_kg > 0
- CO2_per_kg >= 0
- Moisture_resistance: 1–10
- Thermal_resistance: 1–10
- Biodegradation Time (days) >= 1

## Categorical valid sets
- Packaging Type: Box, Pouch, Tray, Wrap, Compostable Sheet
- Material Type: Paper, Plastic, Metal, Bio-based
- Recyclability Category: A, B, C, D

## Uniqueness & integrity
- Material ID must be unique
- No duplicate rows
- No negative weights or dimensions

