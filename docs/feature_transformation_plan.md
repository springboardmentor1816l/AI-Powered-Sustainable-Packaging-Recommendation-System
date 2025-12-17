# Feature Transformation Plan

## Step 1: Input Normalization
All numeric inputs are scaled to a 0–1 range to remove unit bias.

## Step 2: Environmental Scoring
- Convert CO₂ emissions and biodegradation time into green impact scores.
- Apply recyclability category mapping.

## Step 3: Cost Efficiency Calculation
- Normalize costs.
- Adjust using durability and recyclability benefits.
- Penalize inefficient materials.

## Step 4: Suitability Matching
- Match material attributes to product sensitivity profiles.
- Apply penalties for mandatory requirement violations.
- Apply bonuses for strong alignment.

## Step 5: Index Scaling
Final scores are scaled to a 0–100 range for interpretability.

## Step 6: Dataset Integration
Engineered features are appended as new columns to the processed dataset.
