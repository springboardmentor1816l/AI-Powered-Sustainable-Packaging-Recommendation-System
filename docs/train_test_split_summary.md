# Train/Test Split Summary – EcoPackAI

## Dataset Overview
- Dataset: materials_preprocessed_pipeline.csv
- Total records: ~403
- Feature type: Encoded & scaled numeric features

---

## Split Configuration
- Training set: 80%
- Testing set: 20%
- Random state: 42
- Stratification: recommended_material

---

## Split Statistics

### Training Set
- Approx. records: ~322
- Purpose: Model training & cross-validation

### Testing Set
- Approx. records: ~81
- Purpose: Final unbiased model evaluation

---

## Distribution Validation
- Material categories evenly distributed
- No duplication between splits
- No target leakage detected

---

## Conclusion
The dataset split maintains representativeness and ensures fair,
reproducible evaluation for EcoPackAI machine learning models.
