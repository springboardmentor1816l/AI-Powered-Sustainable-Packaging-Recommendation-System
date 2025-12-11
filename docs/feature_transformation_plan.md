
# Feature Transformation Plan

1. Load cleaned dataset
2. For each material record:
   - Standardize numeric inputs (log-scaling for biodegradation where necessary)
   - Map categorical recyclability and material types to numeric scores
   - Compute raw index values as weighted sums
   - Clip and scale to 0..100
3. Fill missing engineered values with conservative medians
4. Save dataset and metadata files
