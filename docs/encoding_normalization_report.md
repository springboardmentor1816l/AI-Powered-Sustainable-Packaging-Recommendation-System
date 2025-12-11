# Encoding & Normalization Report

## Steps Completed

### 1. One-Hot Encoding
- All categorical columns were encoded using OneHotEncoder from scikit-learn
- Unknown categories will be ignored during inference
- Encoder saved at: models/encoders/ohe_encoder.pkl

### 2. Numeric Scaling
- All numeric columns were scaled using MinMaxScaler (range: 0 to 1)
- Scaler saved at: models/scalers/minmax_scaler.pkl

### 3. Output
- Final machine-learning-ready dataset:
  data/model_ready/materials_final_encoded.csv
