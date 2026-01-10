CREATE TABLE IF NOT EXISTS prediction_history (
    id SERIAL PRIMARY KEY,
    request_payload JSONB NOT NULL,
    predicted_cost DOUBLE PRECISION NOT NULL,
    predicted_co2 DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendation_history (
    id SERIAL PRIMARY KEY,
    input_payload JSONB NOT NULL,
    ranked_output JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
