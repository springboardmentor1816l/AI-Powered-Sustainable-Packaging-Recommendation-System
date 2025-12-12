# EcoPackAI Data Dictionary

## Table: materials
| Column                   | Type      | Description |
|---------------------------|----------|-------------|
| material_id               | INT       | Unique identifier for each material |
| material_type             | VARCHAR   | Name of packaging material (paper, bioplastic, PLA, cardboard, sugarcane, etc.) |
| strength_mpa              | FLOAT     | Mechanical strength capacity in MPa |
| weight_capacity           | FLOAT     | Maximum load in kg |
| biodegradability_percent  | FLOAT     | % breakdown in natural environment |
| co2_emission_score        | FLOAT     | Carbon footprint index |
| recyclability_percent     | FLOAT     | Reuse potential in percentage |
| cost_per_kg               | FLOAT     | Cost per kg (INR/USD) |
| industry_use_case         | VARCHAR   | Electronics / Food / Cosmetics / Pharmacy etc |

## Table: products
| Column         | Type      | Description |
|----------------|----------|-------------|
| product_id     | INT       | Unique product identifier |
| product_name   | VARCHAR   | Name of the product |
| category       | VARCHAR   | Product category type |
| product_weight | FLOAT     | Net item weight in kg |
| fragility_index| INT       | Durability / handling care requirement |
| shipping_type  | VARCHAR   | Air / Road / Sea |

## Table: recommendation_logs
| Column                 | Type      | Description |
|------------------------|----------|-------------|
| rec_id                 | INT       | Unique recommendation record ID |
| product_id             | INT       | Foreign key to products table |
| recommended_material_id| INT       | Foreign key to materials table |
| cost_prediction        | FLOAT     | Predicted cost for recommendation |
| co2_prediction         | FLOAT     | Predicted CO₂ impact for recommendation |
| material_rank          | INT       | Rank of recommended material |
| created_at             | TIMESTAMP | Timestamp of recommendation entry |

## Table: users
| Column         | Type      | Description |
|----------------|----------|-------------|
| user_id        | INT       | Unique user identifier |
| username       | VARCHAR   | Username for login |
| email          | VARCHAR   | User email |
| password_hash  | VARCHAR   | Hashed password |
| created_at     | TIMESTAMP | Account creation time |
