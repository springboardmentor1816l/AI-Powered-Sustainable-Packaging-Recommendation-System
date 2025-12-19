# Train-Test Split Summary

## Split Strategy
- Training set: 80%
- Testing set: 20%
- Random seed: 42

## Stratification
- Stratified by Product_Category
- Ensures balanced distribution of product categories

## Leakage Prevention
- Product-material combinations appear in only one split
- No preprocessing or fitting performed on test data
