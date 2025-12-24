# Experiment Reproducibility Notes – EcoPackAI

## Objective
This document outlines the steps taken to ensure reproducibility of
machine learning experiments conducted in EcoPackAI.

---

## Random Seeds
- Train/Test split random_state: 42
- Cross-validation random_state: 42

---

## Environment Details
- Python version: 3.11
- Key libraries:
  - pandas
  - numpy
  - scikit-learn
  - joblib

---

## Assumptions
- Input datasets are preprocessed and validated
- No missing or infinite values exist
- Encoded feature space remains consistent across runs

---

## Reproducibility Guarantees
- Fixed random seeds used throughout
- Preprocessing pipeline saved and reused
- No manual intervention during split or evaluation

---

## Conclusion
These practices ensure consistent, repeatable, and auditable ML
experiments for EcoPackAI.
