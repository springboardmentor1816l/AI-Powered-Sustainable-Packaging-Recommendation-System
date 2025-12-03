# EcoPackAI – Data Dictionary

## 1. Materials Table
| Column | Type | Description |
|--------|------|-------------|
| material_id | INT | Unique identifier for each packaging material |
| material_type | VARCHAR(100) | Name/type of eco-friendly material |
| strength_mpa | FLOAT | Mechanical strength rating in MPa |
| weight_capacity | FLOAT | Maximum weight material can support |
| biodegradability_percent | FLOAT | % of material that biodegrades naturally |
| co2_emission_score | FLOAT | Estimated carbon footprint score |
| recyclability_percent | FLOAT | How much can be recycled (%) |
| cost_per_kg | FLOAT | Cost of the material per kg |
| industry_use_case | VARCHAR(200) | Suitable industry(s) for the material |

---

## 2. Products Table
| Column | Type | Description |
|--------|------|-------------|
| product_id | INT | Unique product ID |
| product_name | VARCHAR(100) | Name/classification of the product |
| category | VARCHAR(100) | Product category (food, electronics, cosmetics, etc.) |
| product_weight | FLOAT | Weight of the product |
| fragility_index | INT | Fragility rating (higher = more delicate) |
| shipping_type | VARCHAR(50) | Shipping mode (Air / Road / Sea) |

---

## 3. Recommendation Logs
| Column | Type | Description |
|--------|------|-------------|
| rec_id | INT | Unique recommendation record |
| product_id | INT | Product referenced in prediction |
| recommended_material_id | INT | Material recommended by ML model |
| cost_prediction | FLOAT | Predicted material cost |
| co2_prediction | FLOAT | Predicted CO₂ emission value |
| material_rank | INT | Ranking among recommended materials |
| created_at | TIMESTAMP | Timestamp of the prediction record |