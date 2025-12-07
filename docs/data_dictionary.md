
# EcoPackAI – Data Dictionary

This document describes the database tables and columns used in the EcoPackAI system for managing eco-friendly packaging materials, product attributes, and AI recommendations.

---

## Table: materials  
Stores information about all eco-friendly packaging materials.

| Column Name | Data Type | Description | Accepted Values / Example |
|------------|------------|-------------|----------------------------|
| material_id | SERIAL (INT) | Unique identifier for each material | Auto-generated |
| material_type | VARCHAR(100) | Type of packaging material | Paper, Bioplastic, PLA, Cardboard |
| strength_mpa | FLOAT | Mechanical strength of the material in MPa | 10.5, 25.2 |
| weight_capacity | FLOAT | Maximum weight the material can hold (kg) | 2.5, 10 |
| biodegradability_percent | FLOAT | Percentage of material that decomposes naturally | 60 – 100 |
| co2_emission_score | FLOAT | Carbon footprint index of the material | 0.2 – 5.0 |
| recyclability_percent | FLOAT | Percentage of material that can be recycled | 50 – 100 |
| cost_per_kg | FLOAT | Cost of material per kilogram | 40, 120, 300 |
| industry_use_case | VARCHAR(200) | Industry where the material is used | Food, Electronics, Cosmetics |

---

## Table: products  
Stores attributes of products that require packaging.

| Column Name | Data Type | Description | Accepted Values / Example |
|------------|------------|-------------|----------------------------|
| product_id | SERIAL (INT) | Unique identifier for each product | Auto-generated |
| product_name | VARCHAR(100) | Name of the product | Mobile Charger, Face Cream |
| category | VARCHAR(100) | Product category | Electronics, Grocery, Cosmetics |
| product_weight | FLOAT | Net weight of the product in kg | 0.5, 2.0 |
| fragility_index | INT | Durability level (1 = Low, 5 = High) | 1 – 5 |
| shipping_type | VARCHAR(50) | Mode of transportation | Air, Road, Sea |

---

## Table: recommendation_logs  
Stores AI model prediction results for recommended packaging materials.

| Column Name | Data Type | Description | Accepted Values / Example |
|------------|------------|-------------|----------------------------|
| rec_id | SERIAL (INT) | Unique ID for each recommendation record | Auto-generated |
| product_id | INT (FK) | Product reference from products table | Valid product_id |
| recommended_material_id | INT (FK) | Material reference from materials table | Valid material_id |
| cost_prediction | FLOAT | Estimated packaging cost for the product | 25.5, 100.0 |
| co2_prediction | FLOAT | Estimated carbon emission for recommendation | 0.3, 1.2 |
| material_rank | INT | Ranking of best recommended material | 1, 2, 3 |
| created_at | TIMESTAMP | Date and time of recommendation generation | Auto-timestamp |

---

##  Purpose of This Data Dictionary  
- Helps developers understand database structure  
- Supports ML dataset preparation  
- Enables frontend-backend integration  
- Used for technical documentation and reports  

---

## Project: EcoPackAI  
AI-Powered Sustainable Packaging Recommendation System  


