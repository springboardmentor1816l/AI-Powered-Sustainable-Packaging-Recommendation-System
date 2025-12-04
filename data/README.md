# EcoPackAI Data Management

This directory contains sample datasets and database setup files for the EcoPackAI sustainable packaging recommendation system.

## 📁 Directory Structure

```
data/
├── material_dataset.csv      # Sample eco-friendly packaging materials
├── product_dataset.csv        # Sample products for testing
└── README.md                  # This file
```

## 📊 Datasets

### material_dataset.csv
Contains 20 eco-friendly packaging materials with attributes:
- **Material Type**: Recycled Cardboard, Bioplastic (PLA), Sugarcane Bagasse, Mushroom Packaging, etc.
- **Physical Properties**: Strength (MPa), weight capacity (kg)
- **Environmental Metrics**: Biodegradability %, CO₂ emission score, recyclability %
- **Economic Data**: Cost per kg
- **Industry Applications**: Electronics, Food, Cosmetics, Pharmacy

### product_dataset.csv
Contains 30 sample products across 4 categories:
- **Electronics**: Smartphones, laptops, tablets, TVs
- **Food**: Canned goods, chocolate, coffee, organic products
- **Cosmetics**: Perfumes, skincare, makeup
- **Pharmacy**: Medicines, supplements, sanitizers

Each product includes weight, fragility index (1-10), and shipping type.

## 🔧 Usage

### Loading Data into PostgreSQL

1. **Create the database schema first**:
```bash
psql -U postgres -d ecopackai_db -f ../backend/db/schema.sql
```

2. **Import material data**:
```bash
psql -U postgres -d ecopackai_db -c "\COPY materials(material_id, material_type, strength_mpa, weight_capacity, biodegradability_percent, co2_emission_score, recyclability_percent, cost_per_kg, industry_use_case) FROM 'material_dataset.csv' DELIMITER ',' CSV HEADER;"
```

3. **Import product data**:
```bash
psql -U postgres -d ecopackai_db -c "\COPY products(product_id, product_name, category, product_weight, fragility_index, shipping_type) FROM 'product_dataset.csv' DELIMITER ',' CSV HEADER;"
```

### Loading Data with Python

```python
import pandas as pd
from sqlalchemy import create_engine

# Create database connection
engine = create_engine('postgresql://username:password@localhost:5432/ecopackai_db')

# Load materials
materials_df = pd.read_csv('data/material_dataset.csv')
materials_df.to_sql('materials', engine, if_exists='append', index=False)

# Load products
products_df = pd.read_csv('data/product_dataset.csv')
products_df.to_sql('products', engine, if_exists='append', index=False)
```

## 📖 Documentation

See [`docs/data_dictionary.md`](../docs/data_dictionary.md) for complete database schema documentation.

## 🔍 Data Sources

These are sample datasets for development and testing. For production deployment:
- Material data sourced from environmental protection databases and material science research
- Product data sourced from industry catalogs and manufacturing specifications
- All metrics validated against ISO and ASTM packaging standards

## 🔄 Updates

To update sequences after manual CSV import:
```sql
SELECT setval('materials_material_id_seq', (SELECT MAX(material_id) FROM materials));
SELECT setval('products_product_id_seq', (SELECT MAX(product_id) FROM products));
```
