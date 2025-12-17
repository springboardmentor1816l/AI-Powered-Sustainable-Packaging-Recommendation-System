✅ 1. Overview

This document summarizes the encoding and normalization steps applied to the cleaned integrated materials dataset.
The goal is to convert raw categorical and numeric fields into a format suitable for machine learning models.

The output consists of:

Encoded dataset (materials_final_encoded.csv)

Saved encoders (OneHotEncoder, LabelEncoder if used)

Saved numeric scaler (MinMaxScaler)

Documentation of transformations

✅ 2. Dataset Used

Input File:

data/processed/cleaned_integrated_materials.csv


Output File:

data/model_ready/materials_final_encoded.csv

✅ 3. Categorical Columns Identified

The following columns were treated as categorical features:

Feature Name	Reason
Packaging Type	Nominal category
Material Type	Nominal category
Recyclability Category	Nominal (low/medium/high)
Supplier Region	Geographic category
Suitable Product Categories	Multi-use categorical description
Recommended Packaging Use Cases	Descriptive categorical label

Encoding Method Used:
✔ One-Hot Encoding (OHE)
Used to handle all nominal categories and avoid imposing artificial ordering.

✅ 4. Numeric Columns Identified and Scaled

All numeric columns except Material ID (identifier) were scaled.

Columns Scaled:

Recyclability (%)

Recycled Content (%)

Reusability (%)

Biodegradation Time (days)

End-of-Life Disposal (%)

Carbon Footprint (kg CO₂/unit)

CO₂ Emission per kg (estimated)

Waste Reduction Impact (%)

Sustainability Target Progress (%)

Load Handling Score

Moisture Resistance Score

Thermal Resistance Score

Cost per Unit (USD)

Annual Usage (units)

Total Material Weight (tons)

Supplier Sustainability Compliance (%)

Scaling Method Used:
✔ MinMaxScaler (0–1 normalization)

Reason:

Preserves distribution shape

Prevents dominance of high-range features

Works well with models like KNN, Neural Nets, Logistic Regression

✅ 5. Encoding & Normalization Methods
🔹 One-Hot Encoding

Applied to all categorical features

Generates binary indicator columns

Handles unknown categories gracefully (handle_unknown='ignore')

Saved as:

models/encoders/ohe_encoder.pkl

🔹 MinMax Scaling

Scaled all numeric features into a range of 0–1:

Formula:

x_scaled = (x - min(x)) / (max(x) - min(x))


Saved as:

models/scalers/numeric_scaler.pkl

✅ 6. Final Dataset Structure

After encoding + normalization:

Category	Count
Original numeric features	~16
Original categorical features	6
One-Hot Encoded columns	depends on unique categories
Final Dataset Total Columns	~40–80 (varies)
✅ 7. Validation Checklist
Validation Step	Status
No missing values remain	✔ Completed
All categorical features encoded	✔ Completed
Numeric features scaled	✔ Completed
Encoders & scalers saved	✔ Completed
Final dataset exported	✔ Completed