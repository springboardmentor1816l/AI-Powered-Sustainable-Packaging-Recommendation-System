# Encoding & Normalization Report – EcoPackAI

## Overview
This report documents the encoding and normalization steps applied during
the Data Cleaning & Preprocessing phase.

## Dataset Used
- cleaned_integrated_materials.csv

## Categorical Encoding
- Nominal categorical features were encoded using One-Hot Encoding.
- Encoding was performed using sklearn's OneHotEncoder.
- Encoder object was saved for reuse during inference.

Saved encoder:
- /models/encoders/ohe_encoder.pkl

## Numerical Normalization
- Numerical features were normalized to a 0–1 range.
- MinMaxScaler was used to handle different value scales.
- Scaler object was saved for reuse during inference.

Saved scaler:
- /models/scalers/numeric_scaler.pkl

## Output
- Final ML-ready dataset exported to:
  /data/model_ready/materials_final_encoded.csv

## Validation
- No missing values remain
- All numeric features scaled
- All categorical features encoded
- Encoders and scalers reusable for prediction pipeline

## Conclusion
The dataset is fully prepared for machine learning model training.
