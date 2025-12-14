Feature Transformation Plan
Project: EcoPackAI

Overview:
This document describes the step-by-step process used to generate
engineered features from the cleaned material dataset.

--------------------------------------------------

Step 1: Load Cleaned Dataset
- Input file: material_cleaned.csv
- Dataset is checked for missing values and duplicates

--------------------------------------------------

Step 2: Normalize Numeric Features
- Min-max normalization is applied
- Safe normalization is used to avoid division by zero
- All normalized values are in the range 0 to 1

--------------------------------------------------

Step 3: Generate CO2 Impact Index
- Normalize CO2 emission score inversely
- Normalize biodegradability percentage
- Normalize recyclability percentage
- Apply weighted aggregation
- Scale final value to 0–100

--------------------------------------------------

Step 4: Generate Cost Efficiency Index
- Normalize cost per kg inversely
- Normalize weight capacity
- Normalize strength
- Apply weighted aggregation
- Scale final value to 0–100

--------------------------------------------------

Step 5: Generate Material Suitability Score
- Normalize strength and weight capacity
- Compute base numeric suitability score
- Apply industry-based adjustment
- Scale final score to 0–100

--------------------------------------------------

Step 6: Validation
- Check for null values
- Ensure all scores lie between 0 and 100
- Confirm logical consistency of scores

--------------------------------------------------

Step 7: Save Output
- Output file: material_engineered.csv
- Dataset is ready for data quality checks,
  database ingestion, and model preparation
