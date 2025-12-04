# Data Dictionary — EcoPackAI

## materials table
| Column | Type | Description |
|--------|------|-------------|
| material_id | SERIAL | Unique identifier for material |
| material_type | VARCHAR(100) | Type of eco-friendly material |
| strength_mpa | FLOAT | Material strength |
| weight_capacity | FLOAT | Max weight capacity |
| biodegradability_percent | FLOAT | How fast it biodegrades |
| co2_emission_score | FLOAT | Carbon footprint |
| recyclability_percent | FLOAT | Recyclability rate |
| cost_per_kg | FLOAT | Price per kg |
| industry_use_case | VARCHAR(200) | Which industry uses it |

## products table
| Column | Type | Description |
|--------|------|-------------|
| product_id | SERIAL | ID of product |
| product_name | VARCHAR(100) | Name of product |
| category | VARCHAR(100) | Product category |
| product_weight | FLOAT | Weight of product |
| fragility_index | INT | Fragility level |
| shipping_type | VARCHAR(50) | Air / Road / Sea shipping |

## recommendation_logs table
| Column | Type | Description |
|--------|------|-------------|
| rec_id | SERIAL | Record ID |
| product_id | INT | Product being recommended |
| recommended_material_id | INT | Material recommended |
| cost_prediction | FLOAT | Predicted cost |
| co2_prediction | FLOAT | Predicted CO₂ |
| material_rank | INT | Ranking |
| created_at | TIMESTAMP | When recommendation was created |
