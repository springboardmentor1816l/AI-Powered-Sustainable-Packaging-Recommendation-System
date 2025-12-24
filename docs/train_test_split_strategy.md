# Train/Test Split Strategy – EcoPackAI

## Overview
This document defines the strategy used to split the ML-ready EcoPackAI
dataset into training and testing subsets. The objective is to ensure
fair model evaluation, representative data distribution, and prevention
of data leakage.

---

## Dataset Used
- Dataset: materials_preprocessed_pipeline.csv
- Type: ML-ready (encoded & scaled)
- Preparation Stage:
  - Product–material integration
  - Data cleaning & feature engineering
  - Target variable definition

---

## Split Ratio
- Training Set: 80%
- Testing Set: 20%

This ratio provides sufficient data for model learning while reserving
a reliable hold-out set for unbiased evaluation.

---

## Representativeness Criteria
The split is designed to maintain representative distributions of:
- Packaging material types
- Industry / product use-cases
- Sustainability characteristics (cost & CO₂ related features)

Randomized splitting ensures that no systematic bias is introduced.

---

## Data Leakage Prevention
- Splitting is performed after preprocessing.
- Identifiers (e.g., material_id) are excluded from features.
- Similar product–material pairs are not duplicated across splits.
- The test set remains completely unseen during training.

---

## Reproducibility
- A fixed random seed is used during splitting.
- The same split can be regenerated consistently for future experiments.

---

## Conclusion
The defined train/test split strategy ensures unbiased evaluation,
representative sampling, and reproducibility for EcoPackAI’s machine
learning workflows.
