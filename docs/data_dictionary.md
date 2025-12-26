| Column                      | Table                | Type      | Description                       |
|-----------------------------|----------------------|-----------|-----------------------------------|
| material_id                 | materials            | INT       | Unique identifier                 |
| material_type               | materials            | VARCHAR   | Material type                     |
| strength_mpa                | materials            | FLOAT     | Strength property                 |
| biodegradability_percent    | materials            | FLOAT     | Eco-friendly score                |
| co2_emission_score          | materials            | FLOAT     | Carbon footprint index            |
| recyclability_percent       | materials            | FLOAT     | Reuse potential                   |
| cost_per_kg                 | materials            | FLOAT     | Pricing                           |
| industry_use_case           | materials            | VARCHAR   | Industry where used               |
| product_id                  | products             | INT       | Product unique ID                 |
| product_name                | products             | VARCHAR   | Name of product                   |
| category                    | products             | VARCHAR   | Product category                  |
| product_weight              | products             | FLOAT     | Net item weight                   |
| fragility_index             | products             | INT       | Handling care requirement         |
| shipping_type               | products             | VARCHAR   | Shipping mode (Air/Road/Sea)      |
| rec_id                      | recommendation_logs  | INT       | Prediction record ID              |
| recommended_material_id     | recommendation_logs  | INT       | Suggested packaging material ID   |
| cost_prediction             | recommendation_logs  | FLOAT     | Predicted cost outcome            |
| co2_prediction              | recommendation_logs  | FLOAT     | Predicted CO2 value               |
| material_rank               | recommendation_logs  | INT       | Rank of recommended material      |
| created_at                  | recommendation_logs  | TIMESTAMP | Timestamp of prediction event     |