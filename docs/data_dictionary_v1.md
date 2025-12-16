# EcoPackAI Data Dictionary

This document describes the structure, purpose, and metadata of all tables and columns used in the EcoPackAI PostgreSQL database.

---

## 📦 **Table: materials**

Stores information about eco-friendly packaging materials and their performance characteristics.

| Column Name              | Data Type     | Description                         | Example          | Allowed Values |
| ------------------------ | ------------- | ----------------------------------- | ---------------- | -------------- |
| material_id              | SERIAL (PK)   | Unique ID for each material         | 1                | Auto-generated |
| material_type            | VARCHAR(100)  | Name/type of packaging material     | "Paper"          | Any text       |
| strength_mpa             | NUMERIC(10,2) | Mechanical strength in MPa          | 22.5             | 0–∞            |
| weight_capacity          | NUMERIC(10,2) | Max load the material can hold (kg) | 5.0              | 0–∞            |
| biodegradability_percent | NUMERIC(5,2)  | Percentage of natural decomposition | 92.5             | 0–100          |
| co2_emission_score       | NUMERIC(10,2) | CO₂ emission index (lower = better) | 12.4             | 0–∞            |
| recyclability_percent    | NUMERIC(5,2)  | Percentage that can be recycled     | 80.0             | 0–100          |
| cost_per_kg              | NUMERIC(10,2) | Material cost per kg                | 45.50            | ≥ 0            |
| industry_use_case        | VARCHAR(200)  | Primary industry use                | "Food Packaging" | Any text       |

---


## 📦 **Table: products**

Contains information about products that need packaging evaluation.

| Column Name     | Data Type     | Description                              | Example       | Allowed Values   |
| --------------- | ------------- | ---------------------------------------- | ------------- | ---------------- |
| product_id      | SERIAL (PK)   | Unique ID for each product               | 1             | Auto-generated   |
| product_name    | VARCHAR(100)  | Name of the product                      | "Smartphone"  | Any text         |
| category        | VARCHAR(100)  | Product category                         | "Electronics" | Any text         |
| product_weight  | NUMERIC(10,2) | Weight in kg                             | 0.45          | ≥ 0              |
| fragility_index | INT           | Fragility rating (higher = more fragile) | 9             | 1–10             |
| shipping_type   | VARCHAR(50)   | Shipping method used                     | "Air"         | Air / Road / Sea |

---

## Engineered Feature Columns

| Column Name           | Data Type     | Description                                      | Example |
|-----------------------|---------------|--------------------------------------------------|---------|
| cii                   | NUMERIC(5,2)  | CO₂ Impact Index (0–100)                         | 74.25   |
| cei                   | NUMERIC(5,2)  | Cost Efficiency Index (0–100)                    | 68.10   |
| mss                   | NUMERIC(5,2)  | Material Suitability Score (0–100)               | 82.50   |
| recommendation_score  | NUMERIC(5,2)  | Final weighted sustainability-performance score  | 78.30   |


## 📊 **Table: recommendation_logs**

Tracks ML-generated packaging recommendations for audits, training, and dashboards.

| Column Name             | Data Type                        | Description                               | Example             | Allowed Values       |
| ----------------------- | -------------------------------- | ----------------------------------------- | ------------------- | -------------------- |
| rec_id                  | SERIAL (PK)                      | Unique recommendation entry               | 101                 | Auto-generated       |
| product_id              | INT (FK → products.product_id)   | Product receiving recommendation          | 5                   | Existing product ID  |
| recommended_material_id | INT (FK → materials.material_id) | Suggested material                        | 2                   | Existing material ID |
| cost_prediction         | NUMERIC(10,2)                    | Predicted packaging cost                  | 12.75               | ≥ 0                  |
| co2_prediction          | NUMERIC(10,2)                    | Predicted CO₂ score                       | 8.5                 | ≥ 0                  |
| material_rank           | INT                              | Ranking among suggested materials         | 1                   | 1–n                  |
| created_at              | TIMESTAMP                        | Timestamp when recommendation was created | 2025-01-10 14:22:18 | Auto-generated       |

---

## ✔ Notes

* Numeric fields use NUMERIC instead of FLOAT for stability in ML and analytics.
* `SERIAL` primary keys auto-increment.
* `created_at` defaults to the current timestamp.
* Foreign keys maintain referential integrity between tables.

---