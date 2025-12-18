# Cross-Validation Strategy

## Method
Stratified K-Fold Cross-Validation

## Configuration
- Number of folds: 5
- Shuffle: Yes
- Random seed: 42
- Stratification column: material_type

## Rationale
Stratification ensures balanced representation of packaging materials
across folds and prevents biased performance estimation.

## Leakage Prevention
Product-material combinations are split once and never shared
between training and validation folds.
