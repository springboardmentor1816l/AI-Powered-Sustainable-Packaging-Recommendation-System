# EcoPackAI — Data Dictionary

This document describes all database tables and fields used in the EcoPackAI system.

---

## 1. Materials Table

| Column                   | Type   | Description                                  |
|-------------------------|--------|----------------------------------------------|
| material_id             | INT    | Auto-generated unique material ID            |
| material_type           | VARCHAR | Material name/type (Paper, PLA, Bioplastic) |
| strength_mpa            | FLOAT  | Mechanical strength                          |
| weight_capacity         | FLOAT  | Maximum weight load the material can carry   |
| biodegradability_percent | FLOAT | % of material that naturally decomposes      |
| co2_emission_score      | FLOAT  | Carbon footprint score                       |
| recyclability_percent   | FLOAT  | % material can be recycled                   |
| cost_per_kg             | FLOAT  | Cost per kg                                  |
| industry_use_case       | VARCHAR | Industry where the material is used         |

---

## 2. Products Table

| Column           | Type   | Description                          |
|------------------|--------|--------------------------------------|
| product_id        | INT    | Unique product ID                   |
| product_name      | VARCHAR | Product name/category              |
| category          | VARCHAR | Product classification             |
| product_weight    | FLOAT  | Weight of the product (kg)         |
| fragility_index   | INT    | Fragile rating (1–10)              |
| shipping_type     | VARCHAR | Air / Road / Sea transport type   |

---

## 3. Recommendation Logs Table

| Column                 | Type      | Description                              |
|------------------------|-----------|------------------------------------------|
| rec_id                 | INT       | Record ID                                 |
| product_id             | INT       | FK → product                              |
| recommended_material_id | INT      | FK → material                             |
| cost_prediction        | FLOAT     | Predicted material cost for product       |
| co2_prediction         | FLOAT     | Carbon impact score                       |
| material_rank          | INT       | Rank of the recommended material          |
| created_at             | TIMESTAMP | Log creation timestamp                    |
