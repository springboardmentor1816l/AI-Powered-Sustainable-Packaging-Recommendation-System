-- backend/db/schema.sql
-- EcoPackAI Database Schema (PostgreSQL)

CREATE SCHEMA IF NOT EXISTS ecopackai;

CREATE TABLE IF NOT EXISTS ecopackai.materials (
    material_id SERIAL PRIMARY KEY,
    material_type VARCHAR(100) NOT NULL,
    strength_mpa REAL,
    weight_capacity REAL,
    biodegradability_percent REAL,
    co2_emission_score REAL,
    recyclability_percent REAL,
    cost_per_kg REAL,
    industry_use_case VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS ecopackai.products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    product_weight REAL,
    fragility_index INT,
    shipping_type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS ecopackai.recommendation_logs (
    rec_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES ecopackai.products(product_id) ON DELETE SET NULL,
    recommended_material_id INT REFERENCES ecopackai.materials(material_id) ON DELETE SET NULL,
    cost_prediction REAL,
    co2_prediction REAL,
    material_rank INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Useful indexes for ML & dashboard queries
CREATE INDEX IF NOT EXISTS idx_material_type ON ecopackai.materials (material_type);
CREATE INDEX IF NOT EXISTS idx_products_category ON ecopackai.products (category);
CREATE INDEX IF NOT EXISTS idx_reclogs_product ON ecopackai.recommendation_logs (product_id);
