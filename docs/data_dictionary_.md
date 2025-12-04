1. Table: materials
| Column                   | Type         | Description                              |
| ------------------------ | ------------ | ---------------------------------------- |
| material_id              | INT (PK)     | Unique material identifier               |
| material_type            | VARCHAR(150) | Type of material (PLA, cardboard, etc.)  |
| strength_mpa             | FLOAT        | Mechanical strength (MPa)                |
| weight_capacity          | FLOAT        | Max load supported (kg)                  |
| biodegradability_percent | FLOAT        | % natural breakdown                      |
| co2_emission_score       | FLOAT        | Carbon footprint value                   |
| recyclability_percent    | FLOAT        | % potential to recycle                   |
| cost_per_kg              | FLOAT        | Price per kg in INR/USD                  |
| industry_use_case        | VARCHAR(200) | Usage category (electronics, food, etc.) |

2. Table: products
| Column          | Type         | Description            |
| --------------- | ------------ | ---------------------- |
| product_id      | INT (PK)     | Unique product ID      |
| product_name    | VARCHAR(150) | Name of product        |
| category        | VARCHAR(150) | Product category       |
| product_weight  | FLOAT        | Weight in kg           |
| fragility_index | INT          | Fragility scale (1–10) |
| shipping_type   | VARCHAR(50)  | Air / Road / Sea       |

3. Table: recommendation_logs
| Column                  | Type                             | Description                            |
| ----------------------- | -------------------------------- | -------------------------------------- |
| rec_id                  | INT (PK)                         | Log entry ID                           |
| product_id              | INT (FK → products.product_id)   | Related product                        |
| recommended_material_id | INT (FK → materials.material_id) | Suggested material                     |
| cost_prediction         | FLOAT                            | Estimated packaging cost               |
| co2_prediction          | FLOAT                            | Projected carbon footprint             |
| material_rank           | INT                              | Rank of the material among suggestions |
| created_at              | TIMESTAMP                        | Date & time of prediction              |
