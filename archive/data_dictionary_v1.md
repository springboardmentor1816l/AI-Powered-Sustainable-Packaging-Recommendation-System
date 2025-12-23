
# Data Dictionary — EcoPackAI

This document describes the database schema fields, their datatypes, and purpose for the EcoPackAI system.

---

## Table: materials

| Column                   | Type        | Description |
|--------------------------|-------------|-------------|
| material_id              | INT (PK)    | Unique identifier for each material |
| material_type            | VARCHAR     | Type of material (Paper, PLA, Bioplastic, Cardboard, Sugarcane, etc.) |
| strength_mpa             | FLOAT       | Mechanical strength measured in MPa |
| weight_capacity          | FLOAT       | Maximum weight the material can safely carry (in kg) |
| biodegradability_percent | FLOAT       | % breakdown in natural environment |
| co2_emission_score       | FLOAT       | Carbon footprint or emission index |
| recyclability_percent    | FLOAT       | % potential of material to be reused |
| cost_per_kg              | FLOAT       | Cost of the material per kilogram |
| industry_use_case        | VARCHAR     | Industries best suited for the material (Electronics, Food, Cosmetics, Pharma, etc.) |

---

## Table: products

| Column         | Type        | Description |
|----------------|-------------|-------------|
| product_id     | INT (PK)    | Unique identifier for each product |
| product_name   | VARCHAR     | Name or classification of the product |
| category       | VARCHAR     | Product category type |
| product_weight | FLOAT       | Net weight of the product in kg |
| fragility_index| INT         | Durability/fragility requirement (higher = more fragile) |
| shipping_type  | VARCHAR     | Shipping mode (Air / Road / Sea) |

---

## Table: recommendation_logs

| Column                  | Type        | Description |
|-------------------------|-------------|-------------|
| rec_id                  | INT (PK)    | Unique recommendation log identifier |
| product_id              | INT (FK)    | Product used for the recommendation |
| recommended_material_id | INT (FK)    | Material recommended by the model |
| cost_prediction         | FLOAT       | Predicted packaging cost |
| co2_prediction          | FLOAT       | Predicted CO₂ emission score |
| material_rank           | INT         | Rank of the recommended material |
| created_at              | TIMESTAMP   | Timestamp of the recommendation generation |


# Data Dictionary – EcoPackAI (Updated)

## Table: materials

| Column Name | Data Type | Description | Value Range / Notes |
|------------|----------|-------------|---------------------|
| material_id | VARCHAR | Unique identifier for packaging material | Alphanumeric |
| material_type | VARCHAR | Type of packaging material | Cardboard, Plastic, Bioplastic, Paper |
| cost_per_kg | FLOAT | Cost of material per kilogram | > 0 |
| recyclability_percent | FLOAT | Percentage of recyclability | 0–100 |
| strength | FLOAT | Load handling / strength score | Relative scale |
| moisture_resistance_score | FLOAT | Resistance to moisture | 0–10 |
| thermal_resistance_score | FLOAT | Resistance to heat | 0–10 |

---

## Engineered Features

| Column Name | Data Type | Description | Value Range |
|------------|----------|-------------|------------|
| CO2_Impact_Index | FLOAT | Environmental sustainability score combining CO₂ emissions, biodegradation, and recyclability | 0–100 |
| Cost_Efficiency_Index | FLOAT | Economic feasibility score based on cost, weight, recyclability, and durability | 0–100 |
| Material_Suitability_Score | FLOAT | Suitability score indicating compatibility with product requirements | 0–100 |

---

## Notes
- Engineered features are derived after data cleaning and preprocessing.
- Higher values indicate better performance or suitability.
- These features are used by the recommendation engine and ML models.
