# Train/Test Split Summary

## Dataset
- Name: product_material_integrated.csv
- Version: v1.0
- Type: Integrated Product × Material dataset

## Split Strategy
- Train/Test Ratio: 80% / 20%
- Stratification: Material Type
- Random Seed: 42

## Integrity Checks
- No product–material pair appears in both splits.
- Product categories, shipping types, and material types are represented in both sets.
- No target leakage observed.

## Outcome
- Training set used for model fitting and cross-validation.
- Test set held out for final unbiased evaluation.
