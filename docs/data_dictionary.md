
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

