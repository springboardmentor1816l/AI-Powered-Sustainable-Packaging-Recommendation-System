# Data Dictionary v2 — EcoPackAI

Source file: `data/processed/cleaned_dataset.csv`

## Dataset summary
- Rows: (fill after running `len(df)`)
- Columns: 23

## Column details

| Column | Type | Description | Example | Nullable | Engineered? | Used in ML? |
|---|---:|---|---|---:|---:|---:|
| Material ID | string | Unique identifier for the material | MAT_0001 | No | No | Yes |
| Packaging Type | string | Packaging format (Box/Pouch/Tray/Wrap) | Box | Yes | No | Yes |
| Material Type | string | Material category (Paper, Plastic, Metal, Bio-based) | Paper | No | No | Yes |
| Suitable Product Categories | string/list | Product categories the material suits | Food;Electronics | Yes | No | Yes |
| Recommended Packaging Use Cases | string | Suggested use-cases | e-commerce packing | Yes | No | Yes |
| Supplier Region | string | Supplier geographic region | India | Yes | No | Yes |
| Recyclability (%) | float | Percent recyclable content | 80.0 | Yes | No | Yes |
| Recyclability Category | string | Graded recyclability A-D | A | Yes | No | Yes |
| Recycled Content (%) | float | Percent recycled material used | 30.0 | Yes | No | Yes |
| Reusability (%) | float | Percent reusability | 20.0 | Yes | No | Yes |
| Biodegradation Time (days) | float/int | Days until biodegradation | 90 | No | No | Yes |
| End-of-Life Disposal (%) | float | % disposed properly | 60.0 | Yes | No | Yes |
| Carbon Footprint (kg CO2/unit) | float | Total CO2 per packaged unit | 0.5 | Yes | No | Yes |
| CO2 Emission per kg (estimated) | float | CO2 per kg of material | 1.2 | No | No | Yes |
| Waste Reduction Impact (%) | float | Estimated waste reduction | 15.0 | Yes | No | Yes |
| Sustainability Target Progress (%) | float | Supplier/Material sustainability progress | 40.0 | Yes | No | Yes |
| Load Handling Score | float | Load handling capability (1-10) | 7 | Yes | No | Yes |
| Moisture Resistance Score | float | Moisture resistance (1-10) | 6 | Yes | No | Yes |
| Thermal Resistance Score | float | Thermal resistance (1-10) | 5 | Yes | No | Yes |
| Cost per Unit (USD) | float | Cost per packaging unit in USD | 0.12 | No | No | Yes |
| Annual Usage (units) | int | Expected annual usage of material | 100000 | Yes | No | Yes |
| Total Material Weight (tons) | float | Total weight used | 12.5 | Yes | No | Yes |
| Supplier Sustainability Compliance (%) | float | Supplier compliance % | 85.0 | Yes | No | Yes |
