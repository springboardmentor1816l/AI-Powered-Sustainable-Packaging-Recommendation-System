# Experiment Reproducibility Notes

## Dataset
- Name: Integrated Product × Material Dataset
- Version: integrated_product_material_v1

## Random Seeds
- Train/Test Split: 42
- Cross-Validation: 42

## Assumptions
- Cartesian join used to generate product–material combinations
- Cost and CO₂ treated as evaluation targets
- No temporal dependency in the dataset

## Reproducibility Guarantee
Using the same dataset version, preprocessing pipeline,
random seed, and metadata files will reproduce identical
splits, folds, and evaluation results.
