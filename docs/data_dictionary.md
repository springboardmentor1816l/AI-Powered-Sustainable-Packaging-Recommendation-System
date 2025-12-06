# Data Dictionary — EcoPackAI

## materials table
| Column                  | Type    | Description |
|------------------------:|:--------|:------------|
| material_id             | INT     | Primary key (auto increment) |
| material_type           | VARCHAR | Material name (e.g., 'Cardboard', 'PLA') |
| strength_mpa            | FLOAT   | Mechanical strength in MPa |
| weight_capacity         | FLOAT   | Max load capacity (kg) |
| biodegradability_percent| FLOAT   | % biodegradability under standard conditions |
| co2_emission_score      | FLOAT   | CO₂ emission index (lower better) |
| recyclability_percent   | FLOAT   | % recyclable material |
| cost_per_kg             | FLOAT   | Cost in INR/USD per kg |
| industry_use_case       | VARCHAR | Typical industries (electronics, food, cosmetics) |

## products table
| Column         | Type    | Description |
|---------------:|:--------|:------------|
| product_id     | INT     | Primary key (auto increment) |
| product_name   | VARCHAR | Product short name |
| category       | VARCHAR | Category (electronics, food, apparel...) |
| product_weight | FLOAT   | Weight in kg |
| fragility_index| INT     | 1–10 (higher = more fragile) |
| shipping_type  | VARCHAR | 'air', 'road', 'sea' |

## recommendation_logs table
| Column             | Type    | Description |
|-------------------:|:--------|:------------|
| rec_id             | INT     | Primary key (auto increment) |
| product_id         | INT     | FK to products.product_id |
| recommended_material_id | INT| FK to materials.material_id |
| cost_prediction    | FLOAT   | Predicted cost for this material & product |
| co2_prediction     | FLOAT   | Predicted CO₂ footprint |
| material_rank      | INT     | Rank (1 = best) |
| created_at         | TIMESTAMP | Record timestamp |
