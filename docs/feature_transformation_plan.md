# Feature Transformation Plan – EcoPackAI

## Overview
This document outlines the step-by-step conceptual transformation process
used to derive engineered sustainability and performance features from
raw packaging material attributes.

The transformations are applied after data cleaning and preprocessing
and before ML model training.

---

## Step 1: Input Dataset Preparation
- Use cleaned and preprocessed materials dataset.
- Ensure no missing values and consistent data types.
- Separate raw attributes and engineered feature targets.

---

## Step 2: CO₂ Impact Index Transformation
- Normalize CO₂ emission values.
- Convert biodegradation time into inverse sustainability score.
- Map recyclability categories to numeric scores.
- Apply material-type sustainability weighting.
- Aggregate weighted components into CO₂ Impact Index (0–100).

---

## Step 3: Cost Efficiency Index Transformation
- Standardize cost-related attributes.
- Compute cost per unit packaging.
- Apply recyclability and reusability benefits.
- Penalize high-cost and low-durability materials.
- Aggregate into Cost Efficiency Index (0–100).

---

## Step 4: Material Suitability Score Transformation
- Define product category requirement profiles.
- Match material attributes against product needs.
- Apply penalties for mandatory requirement failures.
- Apply bonuses for high compatibility and safety.
- Aggregate into Material Suitability Score (0–100).

---

## Step 5: Integration into Dataset
- Append engineered features as new columns.
- Preserve original raw attributes for traceability.
- Validate feature ranges and consistency.

---

## Output
- Dataset enriched with engineered sustainability and suitability metrics.
- Features ready for ML training and recommendation logic.
