
# Experiment Reproducibility Notes

## Data Version
* **Version:** v1.0_engineered_integrated
* **Prerequisites:** Data must be cleaned, engineered, scaled, and encoded according to the documentation from Modules 1-3.

## Splitting and CV Configuration
* **Split Files:** `ml_train_dataset.csv`, `ml_test_dataset.csv`
* **Random Seed:** `42` - Used for the `train_test_split` operation.
* **Cross-Validation:** K-Fold (K=5) will be used for hyperparameter tuning.

## Validation Notes
The split was a simple random shuffle that successfully maintained the mean and variance balance across both primary target variables (Cost and CO2 Indices).
