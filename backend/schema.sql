CREATE TABLE IF NOT EXISTS materials (
  material_id INT AUTO_INCREMENT PRIMARY KEY,
  material_type VARCHAR(200),
  strength_mpa FLOAT,
  weight_capacity FLOAT,
  biodegradability_percent FLOAT,
  co2_emission_score FLOAT,
  recyclability_percent FLOAT,
  cost_per_kg FLOAT,
  industry_use_case VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  product_name VARCHAR(200),
  category VARCHAR(100),
  product_weight FLOAT,
  fragility_index INT,
  shipping_type VARCHAR(50)
);
