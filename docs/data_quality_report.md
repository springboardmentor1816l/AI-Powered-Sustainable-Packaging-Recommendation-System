
# Data Quality Report — EcoPackAI

## 1. Dataset Overview
- Rows: 404
- Columns: 23

## 2. Missing Value Summary (Before Cleaning)
Waste Reduction Impact (%)                1
Carbon Footprint (kg CO2/unit)            1
CO2 Emission per kg (estimated)           1
End-of-Life Disposal (%)                  1
Biodegradation Time (days)                1
Reusability (%)                           1
Recycled Content (%)                      1
Cost per Unit (USD)                       1
Load Handling Score                       1
Moisture Resistance Score                 1
Thermal Resistance Score                  1
Total Material Weight (tons)              1
Annual Usage (units)                      1
Supplier Sustainability Compliance (%)    1
Sustainability Target Progress (%)        1
Recyclability (%)                         0
Supplier Region                           0
Recommended Packaging Use Cases           0
Suitable Product Categories               0
Material Type                             0
Packaging Type                            0
Material ID                               0
Recyclability Category                    0

## 3. Duplicate Rows
- Duplicate rows removed: 0

## 4. Data Types
Material ID                                object
Packaging Type                             object
Material Type                              object
Suitable Product Categories                object
Recommended Packaging Use Cases            object
Supplier Region                            object
Recyclability (%)                           int64
Recyclability Category                     object
Recycled Content (%)                      float64
Reusability (%)                           float64
Biodegradation Time (days)                float64
End-of-Life Disposal (%)                  float64
Carbon Footprint (kg CO2/unit)            float64
CO2 Emission per kg (estimated)           float64
Waste Reduction Impact (%)                float64
Sustainability Target Progress (%)        float64
Load Handling Score                       float64
Moisture Resistance Score                 float64
Thermal Resistance Score                  float64
Cost per Unit (USD)                       float64
Annual Usage (units)                      float64
Total Material Weight (tons)              float64
Supplier Sustainability Compliance (%)    float64

## 5. Cleaning Actions Performed
- Filled numeric missing values with median
- Filled categorical missing values with "Unknown"
- Removed duplicate rows
- Converted negative values to positive where applicable
- Standardized dataset for downstream tasks

## 6. Notes
This cleaned dataset is now ready for:
- Encoding & normalization
- Feature engineering
- Machine learning model training
