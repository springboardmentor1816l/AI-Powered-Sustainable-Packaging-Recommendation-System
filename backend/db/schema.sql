-- ============================================
-- EcoPackAI Database Schema
-- PostgreSQL Database Schema for Sustainable Packaging Recommendation System
-- ============================================

-- Database Creation (Run separately if needed)
-- CREATE DATABASE ecopackai_db;
-- \c ecopackai_db;

-- ============================================
-- TABLE: materials
-- Purpose: Store eco-friendly packaging material information
-- ============================================
CREATE TABLE materials (
    material_id SERIAL PRIMARY KEY,
    material_type VARCHAR(100) NOT NULL,
    strength_mpa FLOAT CHECK (strength_mpa >= 0),
    weight_capacity FLOAT CHECK (weight_capacity >= 0),
    biodegradability_percent FLOAT CHECK (biodegradability_percent >= 0 AND biodegradability_percent <= 100),
    co2_emission_score FLOAT CHECK (co2_emission_score >= 0),
    recyclability_percent FLOAT CHECK (recyclability_percent >= 0 AND recyclability_percent <= 100),
    cost_per_kg FLOAT CHECK (cost_per_kg >= 0),
    industry_use_case VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster material type searches
CREATE INDEX idx_material_type ON materials(material_type);
CREATE INDEX idx_industry_use_case ON materials(industry_use_case);

-- ============================================
-- TABLE: products
-- Purpose: Store product-specific attributes for packaging recommendation
-- ============================================
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    product_weight FLOAT CHECK (product_weight >= 0),
    fragility_index INT CHECK (fragility_index >= 1 AND fragility_index <= 10),
    shipping_type VARCHAR(50) CHECK (shipping_type IN ('Air', 'Road', 'Sea', 'Rail')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for product queries
CREATE INDEX idx_product_category ON products(category);
CREATE INDEX idx_shipping_type ON products(shipping_type);

-- ============================================
-- TABLE: recommendation_logs
-- Purpose: Store ML model prediction results and recommendations
-- ============================================
CREATE TABLE recommendation_logs (
    rec_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    recommended_material_id INT REFERENCES materials(material_id) ON DELETE CASCADE,
    cost_prediction FLOAT,
    co2_prediction FLOAT,
    material_rank INT CHECK (material_rank >= 1),
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for recommendation queries
CREATE INDEX idx_rec_product_id ON recommendation_logs(product_id);
CREATE INDEX idx_rec_material_id ON recommendation_logs(recommended_material_id);
CREATE INDEX idx_rec_created_at ON recommendation_logs(created_at);

-- ============================================
-- TABLE: users (Optional - for future frontend authentication)
-- Purpose: Store user information for dashboard access
-- ============================================
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('admin', 'user', 'viewer')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Create index for user authentication
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_email ON users(email);

-- ============================================
-- TRIGGERS: Auto-update timestamp
-- ============================================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for materials table
CREATE TRIGGER materials_update_timestamp
BEFORE UPDATE ON materials
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Trigger for products table
CREATE TRIGGER products_update_timestamp
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- ============================================
-- Sample Comments for Documentation
-- ============================================
COMMENT ON TABLE materials IS 'Stores information about eco-friendly packaging materials';
COMMENT ON TABLE products IS 'Stores product attributes for packaging recommendations';
COMMENT ON TABLE recommendation_logs IS 'Stores ML model prediction results';
COMMENT ON TABLE users IS 'Stores user authentication data for dashboard access';

COMMENT ON COLUMN materials.strength_mpa IS 'Mechanical strength in MegaPascals (MPa)';
COMMENT ON COLUMN materials.biodegradability_percent IS 'Percentage of material that biodegrades naturally';
COMMENT ON COLUMN materials.co2_emission_score IS 'Carbon footprint index for material production';
COMMENT ON COLUMN products.fragility_index IS 'Product fragility rating from 1 (sturdy) to 10 (very fragile)';
COMMENT ON COLUMN recommendation_logs.material_rank IS 'Ranking of recommended material (1 = best match)';
COMMENT ON COLUMN recommendation_logs.confidence_score IS 'ML model confidence score between 0 and 1';
