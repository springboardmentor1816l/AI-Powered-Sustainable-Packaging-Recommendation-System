CREATE TABLE materials (
    material_id SERIAL PRIMARY KEY,
    material_type VARCHAR(100) NOT NULL,
    strength_mpa NUMERIC(10,2),
    weight_capacity NUMERIC(10,2),
    biodegradability_percent NUMERIC(5,2),
    co2_emission_score NUMERIC(10,2),
    recyclability_percent NUMERIC(5,2),
    cost_per_kg NUMERIC(10,2),
    industry_use_case VARCHAR(200)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    product_weight NUMERIC(10,2),
    fragility_index INT,
    shipping_type VARCHAR(50)
);

CREATE TABLE recommendation_logs (
    rec_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    recommended_material_id INT REFERENCES materials(material_id) ON DELETE SET NULL,
    cost_prediction NUMERIC(10,2),
    co2_prediction NUMERIC(10,2),
    material_rank INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
