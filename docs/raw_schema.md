# Raw Dataset Schema – EcoPackAI

Source File:
EcoPackAI_dataset.csv

Total Rows: 404  
Total Columns: 23  

## Column Definitions (Raw)

- Material ID (string, unique)
- Packaging Type (string, categorical)
- Material Type (string, categorical)
- Suitable Product Categories (string, multi-category text)
- Cost per Kg (float)
- CO2 Emission per Kg (float)
- Moisture Resistance Score (integer, 1–10)
- Thermal Resistance Score (integer, 1–10)
- Biodegradation Time (Days) (integer)
- Material Weight (tons) (float)
- Supplier Sustainability Compliance (%) (float)
- Remaining columns: descriptive / operational metadata

## Notes
- Column names contain spaces
- No guarantees on nulls
- No guarantees on ranges
- No guarantees on uniqueness except Material ID (assumed)
