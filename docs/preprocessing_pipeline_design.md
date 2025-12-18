## Preprocessing Pipeline Design

- Numeric features are median-imputed and standardized
- Categorical features are imputed with mode and one-hot encoded
- Binary features are passed through unchanged
- Target variables are excluded from preprocessing
- Pipeline is reusable for training and inference
