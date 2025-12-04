# EcoPackAI Data Dictionary

## Overview
This document describes the database schema for the **EcoPackAI** system, which recommends sustainable packaging materials based on product attributes and environmental impact metrics.

**Database**: `ecopackai_db`  
**Database Engine**: PostgreSQL  
**Last Updated**: 2025-12-04

---

## Table of Contents
1. [materials](#1-materials)
2. [products](#2-products)
3. [recommendation_logs](#3-recommendation_logs)
4. [users](#4-users)

---

## 1. materials

**Purpose**: Stores information about eco-friendly packaging materials with their environmental and physical properties.

| Column Name | Data Type | Constraints | Description | Example Values |
|-------------|-----------|-------------|-------------|----------------|
| `material_id` | SERIAL | PRIMARY KEY | Unique identifier for each material | 1, 2, 3 |
| `material_type` | VARCHAR(100) | NOT NULL | Name/type of packaging material | Paper, Bioplastic, PLA, Cardboard, Sugarcane |
| `strength_mpa` | FLOAT | CHECK >= 0 | Mechanical strength in MegaPascals (MPa) | 25.5, 40.0, 15.2 |
| `weight_capacity` | FLOAT | CHECK >= 0 | Maximum load capacity in kilograms (kg) | 5.0, 10.0, 2.5 |
| `biodegradability_percent` | FLOAT | CHECK 0-100 | Percentage of material that biodegrades naturally | 85.0, 95.5, 60.0 |
| `co2_emission_score` | FLOAT | CHECK >= 0 | Carbon footprint index (lower is better) | 2.5, 5.0, 1.8 |
| `recyclability_percent` | FLOAT | CHECK 0-100 | Percentage indicating reuse/recycling potential | 70.0, 90.0, 50.0 |
| `cost_per_kg` | FLOAT | CHECK >= 0 | Cost per kilogram in INR/USD | 45.50, 120.00, 80.75 |
| `industry_use_case` | VARCHAR(200) | | Primary industries using this material | Electronics, Food, Cosmetics, Pharmacy |
| `created_at` | TIMESTAMP | DEFAULT NOW | Record creation timestamp | 2025-12-04 10:30:00 |
| `updated_at` | TIMESTAMP | DEFAULT NOW | Record last update timestamp | 2025-12-04 14:20:00 |

**Indexes**:
- `idx_material_type` on `material_type`
- `idx_industry_use_case` on `industry_use_case`

---

## 2. products

**Purpose**: Stores product-specific attributes required for intelligent packaging recommendation.

| Column Name | Data Type | Constraints | Description | Example Values |
|-------------|-----------|-------------|-------------|----------------|
| `product_id` | SERIAL | PRIMARY KEY | Unique identifier for each product | 1, 2, 3 |
| `product_name` | VARCHAR(100) | NOT NULL | Name or classification of product | Smartphone, Laptop, Shampoo Bottle |
| `category` | VARCHAR(100) | | Product category type | Electronics, Cosmetics, Food, Pharmacy |
| `product_weight` | FLOAT | CHECK >= 0 | Net weight of the item in kilograms (kg) | 0.5, 1.2, 0.25 |
| `fragility_index` | INT | CHECK 1-10 | Durability requirement (1=sturdy, 10=very fragile) | 8 (smartphone), 5 (shampoo), 2 (canned food) |
| `shipping_type` | VARCHAR(50) | CHECK values | Mode of transportation | Air, Road, Sea, Rail |
| `created_at` | TIMESTAMP | DEFAULT NOW | Record creation timestamp | 2025-12-04 10:30:00 |
| `updated_at` | TIMESTAMP | DEFAULT NOW | Record last update timestamp | 2025-12-04 14:20:00 |

**Indexes**:
- `idx_product_category` on `category`
- `idx_shipping_type` on `shipping_type`

**Shipping Type Values**: `Air`, `Road`, `Sea`, `Rail`

---

## 3. recommendation_logs

**Purpose**: Stores ML model prediction results and material recommendation rankings for each product.

| Column Name | Data Type | Constraints | Description | Example Values |
|-------------|-----------|-------------|-------------|----------------|
| `rec_id` | SERIAL | PRIMARY KEY | Unique identifier for each recommendation | 1, 2, 3 |
| `product_id` | INT | FOREIGN KEY → products | Reference to product being analyzed | 5, 12, 23 |
| `recommended_material_id` | INT | FOREIGN KEY → materials | Reference to recommended material | 3, 7, 15 |
| `cost_prediction` | FLOAT | | Predicted cost for this material-product pairing | 120.50, 85.75, 200.00 |
| `co2_prediction` | FLOAT | | Predicted CO₂ emissions for this pairing | 3.2, 5.1, 2.8 |
| `material_rank` | INT | CHECK >= 1 | Ranking of material (1 = best match) | 1, 2, 3 |
| `confidence_score` | FLOAT | CHECK 0-1 | ML model confidence score (0 to 1) | 0.95, 0.87, 0.72 |
| `created_at` | TIMESTAMP | DEFAULT NOW | Timestamp when prediction was logged | 2025-12-04 10:30:00 |

**Indexes**:
- `idx_rec_product_id` on `product_id`
- `idx_rec_material_id` on `recommended_material_id`
- `idx_rec_created_at` on `created_at`

**Foreign Key Cascade**: `ON DELETE CASCADE` - deleting a product or material will remove associated recommendation logs.

---

## 4. users

**Purpose**: Stores user authentication and authorization data for dashboard access (optional for future use).

| Column Name | Data Type | Constraints | Description | Example Values |
|-------------|-----------|-------------|-------------|----------------|
| `user_id` | SERIAL | PRIMARY KEY | Unique identifier for each user | 1, 2, 3 |
| `username` | VARCHAR(100) | UNIQUE, NOT NULL | Unique username for login | john_doe, admin_user |
| `email` | VARCHAR(150) | UNIQUE, NOT NULL | User email address | john@example.com |
| `password_hash` | VARCHAR(255) | NOT NULL | Hashed password (bcrypt/argon2) | $2b$12$KIX... |
| `role` | VARCHAR(50) | CHECK values, DEFAULT 'user' | User access level | admin, user, viewer |
| `created_at` | TIMESTAMP | DEFAULT NOW | Account creation timestamp | 2025-12-04 10:30:00 |
| `last_login` | TIMESTAMP | | Last successful login timestamp | 2025-12-04 14:20:00 |

**Indexes**:
- `idx_username` on `username`
- `idx_email` on `email`

**Role Values**: `admin`, `user`, `viewer`

---

## Relationships

```mermaid
erDiagram
    materials ||--o{ recommendation_logs : "recommended in"
    products ||--o{ recommendation_logs : "receives recommendations"
    
    materials {
        int material_id PK
        varchar material_type
        float strength_mpa
        float weight_capacity
        float biodegradability_percent
        float co2_emission_score
    }
    
    products {
        int product_id PK
        varchar product_name
        varchar category
        float product_weight
        int fragility_index
    }
    
    recommendation_logs {
        int rec_id PK
        int product_id FK
        int recommended_material_id FK
        float cost_prediction
        float co2_prediction
        int material_rank
    }
    
    users {
        int user_id PK
        varchar username
        varchar email
        varchar role
    }
```

---

## Data Sources

### Material Dataset Sources
- Environmental protection agency databases
- Material science research papers
- Packaging industry standards (ISO, ASTM)
- Supplier material datasheets

### Product Dataset Sources
- E-commerce product catalogs
- Manufacturing specifications
- Industry categorization standards

---

## Triggers & Automation

### Auto-update Timestamps
- **Trigger**: `materials_update_timestamp` and `products_update_timestamp`
- **Function**: `update_timestamp()`
- **Behavior**: Automatically updates `updated_at` column whenever a record is modified

---

## Notes

1. **Currency Flexibility**: `cost_per_kg` can store values in INR or USD based on deployment region
2. **Fragility Index Scale**: 1 (extremely sturdy, e.g., canned goods) to 10 (extremely fragile, e.g., glass electronics)
3. **CO₂ Emission Score**: Lower values indicate more environmentally friendly materials
4. **Material Rank**: In `recommendation_logs`, rank 1 indicates the best-suited material for that product

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-04 | EcoPackAI Team | Initial schema design |
