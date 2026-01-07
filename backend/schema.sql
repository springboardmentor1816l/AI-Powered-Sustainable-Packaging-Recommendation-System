CREATE TABLE materials (
    material_id SERIAL PRIMARY KEY,
    material_type VARCHAR(100) NOT NULL,
    strength_mpa FLOAT,
    weight_capacity FLOAT,
    biodegradability_percent FLOAT,
    co2_emission_score FLOAT,
    recyclability_percent FLOAT,
    cost_per_kg FLOAT,
    industry_use_case VARCHAR(200)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100),
    product_weight FLOAT,
    fragility_index INT,
    shipping_type VARCHAR(50)
);

CREATE TABLE recommendation_logs (
    rec_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    recommended_material_id INT REFERENCES materials(material_id),
    cost_prediction FLOAT,
    co2_prediction FLOAT,
    material_rank INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
