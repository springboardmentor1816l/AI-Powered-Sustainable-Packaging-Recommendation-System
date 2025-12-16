
# Preprocessing Pipeline Design

## Overview
Reusable preprocessing pipeline built using sklearn ColumnTransformer.

## Numeric Features
- Missing values: Median imputation
- Scaling: StandardScaler

## Categorical Features
- Missing values: Most frequent
- Encoding: OneHotEncoder (handle_unknown=ignore)

## Binary Features
- Converted to numeric (0/1)

## Training Safety
- Pipeline fitted ONLY on training split
- Prevents data leakage

## Output
- Fully numeric, model-ready dataset
