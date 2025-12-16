
# Preprocessing Column Group Definition

This defines the mapping of features to transformers within the ColumnTransformer. Since the data is already cleaned, scaled, and encoded, all features use the 'passthrough' transformation.

## 1. Numeric Passthrough Features (25 Columns)
**Transformation:** Passthrough (Data already scaled [0, 1] using MinMaxScaler)
## 2. OHE Passthrough Features (32 Columns)
**Transformation:** Passthrough (Data already encoded [0, 1] using OneHotEncoder)
## 3. Dropped/Excluded Columns (Not used by the model)
**Transformation:** Drop (Handled by feature selection and remainder='drop')
## 4. Target Variables
These are predicted separately, not processed by the ColumnTransformer.