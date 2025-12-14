Feature Engineering Documentation
Project: EcoPackAI

Objective:
The purpose of feature engineering is to convert raw material attributes into
standardized and meaningful scores that help in sustainability analysis,
cost comparison, and material recommendation.

Feature engineering is applied only on the material dataset.
The product dataset is not modified.

--------------------------------------------------

Engineered Features:

1. CO2 Impact Index (CII)
2. Cost Efficiency Index (CEI)
3. Material Suitability Score (MSS)

All engineered features are scaled between 0 and 100.
Higher score indicates better performance.

--------------------------------------------------

1. CO2 Impact Index (CII)

Purpose:
To measure the environmental sustainability of a material.

Input Columns:
- CO2 emission score
- Biodegradability percentage
- Recyclability percentage

Logic:
- Lower CO2 emission is better
- Higher biodegradability is better
- Higher recyclability is better

Scoring Strategy:
The inputs are normalized using min-max normalization.
CO2 emission is inversely normalized.
Weighted aggregation is applied and scaled to 0–100.

--------------------------------------------------

2. Cost Efficiency Index (CEI)

Purpose:
To evaluate the economic feasibility of a material.

Input Columns:
- Cost per kg
- Weight capacity
- Strength (MPa)

Logic:
- Lower cost per kg increases efficiency
- Higher strength and load capacity increase efficiency

Scoring Strategy:
All numeric inputs are normalized.
Cost is inversely normalized.
A weighted average is calculated and scaled to 0–100.

--------------------------------------------------

3. Material Suitability Score (MSS)

Purpose:
To determine how suitable a material is for a given industry use case.

Input Columns:
- Strength
- Weight capacity
- Industry use case

Logic:
- Numeric performance forms the base score
- Industry use case provides controlled adjustment

Scoring Strategy:
Numeric features are normalized and combined.
Industry category adds a small weighted influence.
Final score is scaled between 0–100.

--------------------------------------------------

Design Assumptions:
- No missing values are present in the dataset
- All engineered features are bounded between 0 and 100
- Feature engineering does not modify raw attributes
- Product dataset is used only for reference and validation

Outcome:
The engineered dataset is suitable for downstream validation,
database ingestion, and machine learning.
