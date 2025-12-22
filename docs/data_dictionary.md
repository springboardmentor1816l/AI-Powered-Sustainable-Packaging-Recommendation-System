# EcoPackAI – Data Dictionary

## Table: materials

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| material_id | SERIAL | Unique identifier for each packaging material |
| material_type | VARCHAR | Type or name of the packaging material |
| strength_mpa | FLOAT | Strength of the material in megapascals |
| weight_capacity | FLOAT | Maximum weight the material can safely carry |
| biodegradability_percent | FLOAT | Percentage showing how biodegradable the material is |
| co2_emission_score | FLOAT | Carbon dioxide emission score of the material |
| recyclability_percent | FLOAT | Percentage showing how recyclable the material is |
| cost_per_kg | FLOAT | Cost of the material per kilogram |
| industry_use_case | VARCHAR | Common industries or use cases where the material is used |


## Table: products

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| product_id | SERIAL | Unique identifier for each product |
| product_name | VARCHAR | Name of the product |
| category | VARCHAR | Category to which the product belongs |
| product_weight | FLOAT | Weight of the product |
| fragility_index | INT | Level of fragility of the product |
| shipping_type | VARCHAR | Mode of shipping such as air, road, or sea |


## Table: recommendation_logs

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| rec_id | SERIAL | Unique identifier for each recommendation record |
| product_id | INT | Reference to the product for which recommendation is made |
| recommended_material_id | INT | Reference to the recommended packaging material |
| cost_prediction | FLOAT | Predicted cost for the selected material |
| co2_prediction | FLOAT | Predicted carbon emission value |
| material_rank | INT | Ranking of the material among alternatives |
| created_at | TIMESTAMP | Date and time when the recommendation was generated |
