# EcoPackAI — Data Dictionary

## Table: materials
| Column Name              | Type    | Description |
|--------------------------|---------|-------------|
| material_id              | INT     | Unique identifier for material |
| material_type            | VARCHAR | Material name/type |
| strength_mpa             | FLOAT   | Mechanical strength |
| weight_capacity          | FLOAT   | Maximum load capability (kg) |
| biodegradability_percent | FLOAT   | % biodegradability |
| co2_emission_score       | FLOAT   | Carbon footprint index |
| recyclability_percent    | FLOAT   | Recyclability percentage |
| cost_per_kg              | FLOAT   | Cost per kilogram |
| industry_use_case        | VARCHAR | Applicable industries |

---

## Table: products
| Column Name      | Type    | Description |
|------------------|---------|-------------|
| product_id       | INT     | Unique product ID |
| product_name     | VARCHAR | Product name |
| category         | VARCHAR | Category (Food, Electronics, etc.) |
| product_weight   | FLOAT   | Weight in kg |
| fragility_index  | INT     | Fragility score (1–10) |
| shipping_type    | VARCHAR | Air, Road, or Sea |

---

## Table: recommendation_logs
| Column Name             | Type      | Description |
|-------------------------|-----------|-------------|
| rec_id                  | INT       | Log entry ID |
| product_id              | INT (FK)  | References products |
| recommended_material_id | INT (FK)  | References materials |
| cost_prediction         | FLOAT     | Predicted cost |
| co2_prediction          | FLOAT     | Predicted CO₂ emissions |
| material_rank           | INT       | Rank of material (1 = best) |
| created_at              | TIMESTAMP | Timestamp of recommendation |
