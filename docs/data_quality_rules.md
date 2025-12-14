# Data Quality Rules – EcoPackAI

## Mandatory Columns (No Nulls Allowed)
- Material ID
- Material Type
- Cost/kg
- CO₂ Emission per kg

## Optional Columns (Nulls Allowed)
- Supplier Notes
- Special Handling

## Value Range Rules
- Cost/kg > 0
- CO₂ emission per kg ≥ 0
- Moisture resistance score: 1–10
- Thermal resistance score: 1–10
- Biodegradation days ≥ 1

## Categorical Rules
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

## Uniqueness & Integrity Rules
- Material ID must be unique
- No duplicate rows
- No negative weights or dimensions
