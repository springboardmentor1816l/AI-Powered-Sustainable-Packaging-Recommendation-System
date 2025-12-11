# Data Quality Rules

## 1. Mandatory Columns
- Material ID
- Material Type
- Cost per kg
- CO₂ emission per kg

## 2. Missing Value Rules
- No nulls in required fields
- Optional fields allowed to have nulls: Supplier Notes, Special Handling

## 3. Value Range Rules
- Cost/kg > 0
- CO₂ emission per kg ≥ 0
- Moisture resistance score: 1–10
- Thermal resistance: 1–10
- Biodegradation days ≥ 1

## 4. Categorical Rules
- Packaging Type: Box, Pouch, Tray, Wrap, Compostable Sheet
- Material Type: Paper, Plastic, Metal, Bio-based
- Recyclability Category: A, B, C, D

## 5. Integrity Rules
- Material ID must be unique
- No duplicate rows
- No negative weights or dimensions
