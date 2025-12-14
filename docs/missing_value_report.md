# Missing Value Handling Report

## Dataset
Integrated Materials Dataset

## Dataset Overview
- Total records: 404
- Total columns: 23
- Data types:
  - Numeric columns: 16 (float64 + int64)
  - Categorical columns: 7 (object)

## Missing Value Summary
Based on `df.info()` and `df.isnull().sum()`:

### Columns with Missing Values (1 missing value each)
- Recycled Content (%)
- Reusability (%)
- Biodegradation Time (days)
- End-of-Life Disposal (%)
- Carbon Footprint (kg CO2/unit)
- CO2 Emission per kg (estimated)
- Waste Reduction Impact (%)
- Sustainability Target Progress (%)
- Load Handling Score
- Moisture Resistance Score
- Thermal Resistance Score
- Cost per Unit (USD)
- Annual Usage (units)
- Total Material Weight (tons)
- Supplier Sustainability Compliance (%)

### Columns with No Missing Values
- Material ID
- Packaging Type
- Material Type
- Suitable Product Categories
- Recommended Packaging Use Cases
- Supplier Region
- Recyclability (%)
- Recyclability Category

## Missing Value Handling Strategy
- All affected columns are **numeric**
- Each column contains only **one missing value**
- **Median imputation** was applied to numeric columns to avoid the effect of outliers
- No rows were removed since missing data volume was minimal

## Result
- All missing values were successfully handled
- Final dataset contains **404 rows with no null values**
- Cleaned dataset saved to:
  `/data/processed/cleaned_integrated_materials.csv`

## Conclusion
The dataset is now clean, consistent, and ready for feature encoding and normalization in the next preprocessing stage.
