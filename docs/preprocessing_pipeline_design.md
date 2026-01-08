# Preprocessing Pipeline Design

This preprocessing pipeline is built using Scikit-learn's ColumnTransformer to ensure
consistent data transformation during training and inference.

## Numeric Features
- Missing values handled using median imputation
- Features scaled using StandardScaler

## Categorical Features
- Missing values handled using most frequent category
- One-Hot Encoding applied
- Unknown categories safely ignored

## Binary Features
- Converted to numeric format
- Missing values handled using most frequent value

## Key Benefits
- Prevents data leakage
- Ensures reproducibility
- Enables seamless deployment
- Produces model-ready data
