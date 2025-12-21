# Train / Test Split Summary

## Dataset
- Source: integrated_dataset.csv
- Total rows: ~600k (product × material combinations)

## Split Strategy
- Train: 80%
- Test: 20%
- Random Seed: 42

## Stratification
Data was stratified by:
- Product category

This ensures balanced representation across product types.

## Leakage Prevention
- No shared rows between train and test
- No target columns included in features
