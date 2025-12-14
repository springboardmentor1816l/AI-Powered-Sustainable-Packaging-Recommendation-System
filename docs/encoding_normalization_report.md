# Encoding & Normalization Report

## Categorical Encoding
- One-Hot Encoding applied to all categorical features
- Encoding used for nominal variables with no inherent order
- Encoder saved for reuse during inference

## Numeric Normalization
- Min-Max Scaling applied to all numeric features
- Scaled values range between 0 and 1
- Scaler saved for inference pipeline

## Output Files
- Encoded dataset:
  /data/model_ready/materials_final_encoded.csv
- One-Hot Encoder:
  /models/encoders/ohe_encoder.pkl
- Numeric Scaler:
  /models/scalers/numeric_scaler.pkl

## Validation
- No missing values
- All features converted to numeric format
- Dataset ready for machine learning models
