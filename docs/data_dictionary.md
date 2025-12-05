# EcoPackAI — Data Dictionary

---

## TABLE: materials
| Column                     | Type    | Description                         |
|----------------------------|---------|-------------------------------------|
| material_id                | INT     | Unique material identifier          |
| material_type              | VARCHAR | Type of packaging material          |
| strength_mpa               | FLOAT   | Mechanical strength                 |
| weight_capacity            | FLOAT   | Maximum supportable load (kg)       |
| biodegradability_percent   | FLOAT   | % biodegradation                    |
| co2_emission_score         | FLOAT   | Carbon footprint score              |
| recyclability_percent      | FLOAT   | % recyclability                     |
| cost_per_kg                | FLOAT   | Cost per kilogram                   |
| industry_use_case          | VARCHAR | Suitable industry category          |

---

## TABLE: products
| Column            | Type    | Description                     |
|-------------------|---------|---------------------------------|
| product_id        | INT     | Unique product identifier       |
| product_name      | VARCHAR | Product name                    |
| category          | VARCHAR | Product category                |
| product_weight    | FLOAT   | Weight of product (kg)          |
| fragility_index   | INT     | Fragility rating (1–10)         |
| shipping_type     | VARCHAR | Air / Road / Sea                |

---

## TABLE: recommendation_logs
| Column                   | Type      | Description                                 |
|--------------------------|-----------|---------------------------------------------|
| rec_id                   | INT       | Unique recommendation log ID                |
| product_id               | INT (FK)  | Reference to products table                 |
| recommended_material_id  | INT (FK)  | Reference to materials table                |
| cost_prediction          | FLOAT     | Predicted packaging cost                    |
| co2_prediction           | FLOAT     | Predicted CO₂ emissions                     |
| material_rank            | INT       | Rank of recommended material (1 = best)     |
| created_at               | TIMESTAMP | Time when recommendation was created        |
