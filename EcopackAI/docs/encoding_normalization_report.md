# Encoding & Normalization Report — EcoPackAI

## Input / Output
- Input cleaned dataset: `EcopackAI\data\processed\cleaned_integrated_materials.csv`
- Output encoded dataset: `EcopackAI\data\model_ready\materials_final_encoded.csv`

## Encoding Strategy
- Nominal categorical features: **One-Hot Encoding**
- Unknown categories during inference: handled with `handle_unknown='ignore'`

## Normalization Strategy
- Numeric features scaled using **MinMaxScaler (0–1 scaling)**

## Saved Artifacts
- OneHotEncoder saved at: `EcopackAI\models\encoders\ohe_encoder.pkl`
- Numeric scaler saved at: `EcopackAI\models\scalers\numeric_scaler.pkl`

## Columns Encoded
- Total categorical columns: 7
- Total numeric columns: 16
- Final feature count after encoding: 450
