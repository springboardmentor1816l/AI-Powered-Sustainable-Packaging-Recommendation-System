# Material Ranking Logic Documentation

## Overview

The Material Ranking module is a core component of the EcoPackAI Recommendation Engine that evaluates and ranks sustainable packaging materials based on multiple criteria including environmental impact (CO₂ emissions), cost efficiency, material suitability, and sustainability compliance.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Ranking Methodology](#ranking-methodology)
3. [Configuration](#configuration)
4. [Usage Guide](#usage-guide)
5. [API Reference](#api-reference)
6. [Validation & Testing](#validation--testing)
7. [Examples](#examples)

---

## System Architecture

### Components

```
┌─────────────────────────────────────────────────────────┐
│                   Material Ranking System               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │  Input Data  │      │ Predictions  │               │
│  │  Features    │      │ Cost & CO₂   │               │
│  └──────┬───────┘      └──────┬───────┘               │
│         │                     │                        │
│         └──────────┬──────────┘                        │
│                    │                                   │
│         ┌──────────▼──────────┐                        │
│         │  Constraint Filter  │                        │
│         │  (Business Rules)   │                        │
│         └──────────┬──────────┘                        │
│                    │                                   │
│         ┌──────────▼──────────┐                        │
│         │   Normalization     │                        │
│         │   (Min-Max/Z-Score) │                        │
│         └──────────┬──────────┘                        │
│                    │                                   │
│         ┌──────────▼──────────┐                        │
│         │  Score Calculation  │                        │
│         │  (Weighted Sum)     │                        │
│         └──────────┬──────────┘                        │
│                    │                                   │
│         ┌──────────▼──────────┐                        │
│         │  Ranking & Sorting  │                        │
│         └──────────┬──────────┘                        │
│                    │                                   │
│         ┌──────────▼──────────┐                        │
│         │  Top-N Selection    │                        │
│         └──────────┬──────────┘                        │
│                    │                                   │
│         ┌──────────▼──────────┐                        │
│         │  Export Rankings    │                        │
│         └─────────────────────┘                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Input Stage**: Load feature dataset and model predictions
2. **Filtering Stage**: Apply business constraints to remove invalid materials
3. **Normalization Stage**: Scale all features to comparable ranges [0, 1]
4. **Scoring Stage**: Calculate weighted composite score
5. **Ranking Stage**: Sort materials by score
6. **Output Stage**: Export top-N recommendations with explanations

---

## Ranking Methodology

### Composite Ranking Score

The ranking system uses a **weighted multi-criteria scoring approach**:

```
Final Score = Σ (weight_i × normalized_feature_i)
```

Where:
- Each criterion has a configurable weight
- Features are normalized to [0, 1] scale
- Lower-is-better metrics (cost, CO₂) are inverted: `score = 1 - normalized_value`
- Higher-is-better metrics are used directly: `score = normalized_value`

### Ranking Criteria

| Criterion | Weight (Balanced) | Direction | Description |
|-----------|-------------------|-----------|-------------|
| **CO₂ Emission** | 30% | Lower is better | Environmental impact per kg |
| **Cost** | 30% | Lower is better | Cost per unit (USD) |
| **Material Suitability** | 25% | Higher is better | Engineered suitability score |
| **Recyclability** | 10% | Higher is better | Recyclability percentage |
| **Sustainability Compliance** | 5% | Higher is better | Supplier compliance |

### Ranking Modes

The system supports three pre-configured ranking modes:

#### 1. **Sustainability-First Mode**
Prioritizes environmental impact over cost.

```yaml
weights:
  co2_emission: 40%
  cost: 20%
  material_suitability: 25%
  recyclability: 10%
  sustainability_compliance: 5%
```

**Use Case**: Organizations with strong environmental commitments, eco-conscious brands.

#### 2. **Cost-First Mode**
Prioritizes cost efficiency while maintaining minimum sustainability standards.

```yaml
weights:
  co2_emission: 15%
  cost: 50%
  material_suitability: 20%
  recyclability: 10%
  sustainability_compliance: 5%
```

**Use Case**: Budget-constrained projects, cost-sensitive markets.

#### 3. **Balanced Mode** (Default)
Balances environmental impact and cost equally.

```yaml
weights:
  co2_emission: 30%
  cost: 30%
  material_suitability: 25%
  recyclability: 10%
  sustainability_compliance: 5%
```

**Use Case**: General recommendations, balanced decision-making.

---

## Configuration

### Configuration File Structure

The system is configured via `config/ranking_weights.yaml`:

```yaml
# Ranking mode selection
ranking_mode: "balanced"  # Options: sustainability_first, cost_first, balanced

# Weights for each mode
weights:
  sustainability_first:
    co2_emission: 0.40
    cost: 0.20
    material_suitability: 0.25
    recyclability: 0.10
    sustainability_compliance: 0.05
  
  cost_first:
    co2_emission: 0.15
    cost: 0.50
    material_suitability: 0.20
    recyclability: 0.10
    sustainability_compliance: 0.05
  
  balanced:
    co2_emission: 0.30
    cost: 0.30
    material_suitability: 0.25
    recyclability: 0.10
    sustainability_compliance: 0.05

# Business constraints
constraints:
  min_recyclability_percent: 30.0
  max_cost_per_unit: 100.0
  min_load_handling_score: 40.0
  min_moisture_resistance_score: 30.0
  min_thermal_resistance_score: 30.0
  min_material_suitability_score: 40.0
  min_sustainability_compliance_percent: 50.0

# Normalization method
normalization:
  method: "min_max"  # Options: min_max, z_score, robust

# Output settings
output:
  top_n_recommendations: 5
  include_explanations: true
  export_formats: ["csv", "json"]
```

### Business Constraints

Constraints act as **hard filters** - materials failing any constraint are excluded before ranking:

| Constraint | Default | Purpose |
|------------|---------|---------|
| `min_recyclability_percent` | 30% | Ensure minimum environmental responsibility |
| `max_cost_per_unit` | $100 | Control budget limits |
| `min_load_handling_score` | 40 | Ensure structural integrity |
| `min_moisture_resistance_score` | 30 | Prevent moisture damage |
| `min_thermal_resistance_score` | 30 | Ensure thermal protection |
| `min_material_suitability_score` | 40 | Guarantee basic suitability |
| `min_sustainability_compliance_percent` | 50% | Enforce supplier standards |

### Normalization Methods

#### Min-Max Normalization (Default)
```python
normalized = (value - min) / (max - min)
```
- Range: [0, 1]
- Best for: Standard distributions, no outliers

#### Z-Score Normalization
```python
normalized = (value - mean) / std_dev
```
- Clips to [-3, 3] then rescales to [0, 1]
- Best for: Gaussian distributions, handling outliers

#### Robust Normalization
```python
normalized = (value - median) / IQR
```
- Uses median and interquartile range (IQR)
- Best for: Skewed distributions, extreme outliers

---

## Usage Guide

### Basic Usage

```python
from src.recommendation.ranker import MaterialRanker

# Initialize ranker with configuration
ranker = MaterialRanker(
    config_path='config/ranking_weights.yaml',
    ranking_mode='balanced'
)

# Run complete ranking pipeline
df_ranked = ranker.run_ranking_pipeline(
    data_path='data/ml_ready/X_raw.csv',
    predictions_path='outputs/predictions.csv',  # Optional
    output_path='outputs/material_rankings.csv',
    group_by=None,  # Or 'packaging_type', 'product_category', etc.
    top_n=10
)

# View top recommendations
print(df_ranked.head())
```

### Advanced Usage

#### 1. Custom Weight Configuration

```python
# Switch ranking mode dynamically
ranker.ranking_mode = 'sustainability_first'
ranker.weights = ranker.config_weights['sustainability_first']

# Or create custom weights
ranker.weights = {
    'co2_emission': 0.35,
    'cost': 0.25,
    'material_suitability': 0.25,
    'recyclability': 0.10,
    'sustainability_compliance': 0.05
}
```

#### 2. Group-Based Ranking

```python
# Rank materials separately for each packaging type
df_ranked = ranker.rank_materials(
    df_features,
    group_by='packaging_type'
)

# Get top 5 materials for each packaging type
df_top = ranker.get_top_recommendations(
    df_ranked,
    top_n=5,
    group_by='packaging_type'
)
```

#### 3. Custom Constraint Adjustment

```python
# Adjust constraints for specific use case
ranker.constraints['min_recyclability_percent'] = 50.0
ranker.constraints['max_cost_per_unit'] = 50.0

# Re-run ranking
df_ranked = ranker.rank_materials(df_features)
```

#### 4. Export in Multiple Formats

```python
# Export as CSV
ranker.export_rankings(df_ranked, 'outputs/rankings.csv', format='csv')

# Export as JSON
ranker.export_rankings(df_ranked, 'outputs/rankings.json', format='json')

# Export as Excel
ranker.export_rankings(df_ranked, 'outputs/rankings.xlsx', format='excel')
```

---

## API Reference

### `MaterialRanker` Class

#### Constructor

```python
MaterialRanker(config_path: Optional[str] = None, ranking_mode: str = "balanced")
```

**Parameters:**
- `config_path`: Path to YAML configuration file
- `ranking_mode`: Ranking mode ('sustainability_first', 'cost_first', 'balanced')

#### Methods

##### `apply_constraints(df: pd.DataFrame) -> pd.DataFrame`
Apply business constraints to filter materials.

**Returns:** Filtered DataFrame with only valid materials

##### `normalize_features(df: pd.DataFrame, features: List[str]) -> pd.DataFrame`
Normalize features to [0, 1] scale.

**Parameters:**
- `df`: Input DataFrame
- `features`: List of feature names to normalize

**Returns:** DataFrame with normalized features

##### `calculate_ranking_score(df: pd.DataFrame) -> pd.DataFrame`
Calculate composite ranking score for each material.

**Returns:** DataFrame with `ranking_score` column added

##### `rank_materials(df: pd.DataFrame, group_by: Optional[str] = None) -> pd.DataFrame`
Rank materials based on composite scores.

**Parameters:**
- `df`: DataFrame with materials and features
- `group_by`: Optional column to group by

**Returns:** DataFrame with `rank` column added

##### `get_top_recommendations(df_ranked: pd.DataFrame, top_n: Optional[int] = None, group_by: Optional[str] = None) -> pd.DataFrame`
Get top N recommended materials.

**Parameters:**
- `df_ranked`: Ranked DataFrame
- `top_n`: Number of top materials (default from config)
- `group_by`: Optional grouping column

**Returns:** DataFrame with top N materials

##### `generate_explanation(material_row: pd.Series) -> str`
Generate human-readable explanation for ranking.

**Returns:** Explanation string

##### `export_rankings(df_ranked: pd.DataFrame, output_path: str, format: str = 'csv', include_explanations: bool = None)`
Export rankings to file.

**Parameters:**
- `df_ranked`: Ranked DataFrame
- `output_path`: Output file path
- `format`: Export format ('csv', 'json', 'excel')
- `include_explanations`: Include explanation column

##### `run_ranking_pipeline(data_path: str, predictions_path: Optional[str] = None, output_path: str = 'outputs/material_rankings.csv', group_by: Optional[str] = None, top_n: Optional[int] = None) -> pd.DataFrame`
Run complete ranking pipeline.

**Parameters:**
- `data_path`: Path to feature dataset
- `predictions_path`: Optional path to predictions
- `output_path`: Output file path
- `group_by`: Optional grouping column
- `top_n`: Number of top materials

**Returns:** DataFrame with ranked materials

---

## Validation & Testing

### Validation Checklist

✅ **Ranking Logic Validation**
- [ ] Weights sum to 1.0 for all ranking modes
- [ ] Normalization produces values in [0, 1]
- [ ] Score calculation is deterministic
- [ ] Rankings are consistent across multiple runs

✅ **Constraint Validation**
- [ ] All constraints are properly enforced
- [ ] Materials failing constraints are filtered
- [ ] Edge cases (all materials filtered) handled gracefully

✅ **Output Validation**
- [ ] Top-N selection returns correct number of materials
- [ ] Grouped ranking works correctly
- [ ] Export formats are valid and readable
- [ ] Explanations are informative and accurate

✅ **Performance Validation**
- [ ] Handles large datasets (>10,000 materials) efficiently
- [ ] Grouping operation scales linearly
- [ ] Memory usage is reasonable

### Test Cases

#### Test 1: Basic Ranking
```python
# Test basic ranking without predictions
ranker = MaterialRanker(config_path='config/ranking_weights.yaml')
df = pd.read_csv('data/ml_ready/X_raw.csv')
df_ranked = ranker.rank_materials(df)

assert 'rank' in df_ranked.columns
assert 'ranking_score' in df_ranked.columns
assert df_ranked['rank'].min() == 1
assert df_ranked['ranking_score'].max() <= 1.0
```

#### Test 2: Constraint Filtering
```python
# Test that constraints filter correctly
initial_count = len(df)
df_filtered = ranker.apply_constraints(df)

assert len(df_filtered) <= initial_count
assert df_filtered['recyclability_percent'].min() >= ranker.constraints['min_recyclability_percent']
```

#### Test 3: Deterministic Results
```python
# Test that ranking is deterministic
df_ranked_1 = ranker.rank_materials(df)
df_ranked_2 = ranker.rank_materials(df)

assert df_ranked_1['rank'].equals(df_ranked_2['rank'])
assert df_ranked_1['ranking_score'].equals(df_ranked_2['ranking_score'])
```

#### Test 4: Group Ranking
```python
# Test group-based ranking
df_grouped = ranker.rank_materials(df, group_by='packaging_type')

for group in df_grouped['packaging_type'].unique():
    group_data = df_grouped[df_grouped['packaging_type'] == group]
    assert group_data['rank'].min() == 1  # Each group has rank 1
```

---

## Examples

### Example 1: Sustainability-First Recommendation

```python
# Initialize with sustainability-first mode
ranker = MaterialRanker(
    config_path='config/ranking_weights.yaml',
    ranking_mode='sustainability_first'
)

# Load data
df = pd.read_csv('data/ml_ready/X_raw.csv')

# Tighten environmental constraints
ranker.constraints['min_recyclability_percent'] = 70.0

# Rank materials
df_ranked = ranker.rank_materials(df)

# Get top 10 most sustainable materials
df_top = ranker.get_top_recommendations(df_ranked, top_n=10)

print("\nTop 10 Most Sustainable Materials:")
print(df_top[['rank', 'material_type', 'ranking_score', 'recyclability_percent', 'co2_emission_per_kg_estimated']])
```

**Expected Output:**
```
Top 10 Most Sustainable Materials:
   rank           material_type  ranking_score  recyclability_percent  co2_emission_per_kg_estimated
0     1  Recycled Cardboard             0.892                   95.0                           0.5
1     2  Biodegradable Plastic          0.847                   85.0                           1.2
2     3  Bamboo Fiber                   0.823                   90.0                           1.8
...
```

### Example 2: Cost-Optimized Recommendation

```python
# Initialize with cost-first mode
ranker = MaterialRanker(
    config_path='config/ranking_weights.yaml',
    ranking_mode='cost_first'
)

# Load data with predictions
df = pd.read_csv('data/ml_ready/X_raw.csv')
predictions = pd.read_csv('outputs/predictions.csv')
df['predicted_cost'] = predictions['predicted_cost']

# Set budget constraint
ranker.constraints['max_cost_per_unit'] = 25.0

# Rank materials
df_ranked = ranker.rank_materials(df)

# Get top 5 cost-effective materials
df_top = ranker.get_top_recommendations(df_ranked, top_n=5)

print("\nTop 5 Cost-Effective Materials:")
print(df_top[['rank', 'material_type', 'ranking_score', 'predicted_cost', 'recyclability_percent']])
```

### Example 3: Packaging-Type Specific Recommendations

```python
# Balanced mode with grouping
ranker = MaterialRanker(ranking_mode='balanced')

# Load data
df = pd.read_csv('data/ml_ready/X_raw.csv')

# Rank materials for each packaging type
df_ranked = ranker.rank_materials(df, group_by='packaging_type')

# Get top 3 for each packaging type
df_top = ranker.get_top_recommendations(df_ranked, top_n=3, group_by='packaging_type')

# Display recommendations by packaging type
for ptype in df_top['packaging_type'].unique():
    print(f"\n=== Best Materials for {ptype} ===")
    subset = df_top[df_top['packaging_type'] == ptype]
    print(subset[['rank', 'material_type', 'ranking_score']])
```

### Example 4: Custom Scoring with Product Requirements

```python
# Custom configuration for fragile products
ranker = MaterialRanker(config_path='config/ranking_weights.yaml')

# Adjust constraints for fragile items
ranker.constraints['min_load_handling_score'] = 70.0
ranker.constraints['min_moisture_resistance_score'] = 60.0

# Custom weights emphasizing protection
ranker.weights = {
    'co2_emission': 0.20,
    'cost': 0.20,
    'material_suitability': 0.45,  # Emphasize suitability
    'recyclability': 0.10,
    'sustainability_compliance': 0.05
}

# Filter for specific product category
df = pd.read_csv('data/ml_ready/X_raw.csv')
df_fragile = df[df['suitable_product_categories'].str.contains('Fragile', na=False)]

# Rank
df_ranked = ranker.rank_materials(df_fragile)
df_top = ranker.get_top_recommendations(df_ranked, top_n=5)

print("\nBest Materials for Fragile Products:")
print(df_top[['rank', 'material_type', 'load_handling_score', 'moisture_resistance_score']])
```

---

## Performance Considerations

### Computational Complexity

- **Constraint Filtering**: O(n) where n = number of materials
- **Normalization**: O(n × m) where m = number of features
- **Score Calculation**: O(n × k) where k = number of criteria
- **Ranking**: O(n log n) for sorting
- **Grouped Ranking**: O(n log n + g × n) where g = number of groups

### Memory Usage

For typical datasets:
- 1,000 materials: ~5 MB
- 10,000 materials: ~50 MB
- 100,000 materials: ~500 MB

### Optimization Tips

1. **Filter Early**: Apply constraints before normalization to reduce dataset size
2. **Batch Processing**: For very large datasets, process in batches
3. **Feature Selection**: Only normalize features actually used in ranking
4. **Caching**: Cache normalized features if running multiple ranking modes

---

## Troubleshooting

### Common Issues

#### Issue 1: All materials filtered out
**Symptom**: `apply_constraints()` returns empty DataFrame

**Solution:**
- Review constraint thresholds in config
- Check data quality (missing values, outliers)
- Temporarily relax constraints to identify bottleneck

```python
# Debug constraint filtering
df_initial = df.copy()
for constraint, threshold in ranker.constraints.items():
    df_filtered = ranker.apply_constraints(df_initial)
    print(f"{constraint}: {len(df_filtered)} materials pass")
```

#### Issue 2: Rankings don't change with different modes
**Symptom**: Same materials ranked #1 across all modes

**Solution:**
- Verify weights are loaded correctly
- Check if features have sufficient variance
- Ensure predictions are included if expected

```python
# Verify weights
print(f"Current weights: {ranker.weights}")
print(f"Weight sum: {sum(ranker.weights.values())}")
```

#### Issue 3: Scores all near 0 or 1
**Symptom**: Ranking scores clustered at extremes

**Solution:**
- Check normalization method
- Verify input data ranges
- Try different normalization method (z_score, robust)

```python
# Check feature distributions
for feature in ['cost_per_unit_usd', 'co2_emission_per_kg_estimated']:
    print(f"{feature}: min={df[feature].min()}, max={df[feature].max()}, mean={df[feature].mean()}")
```

---

## Future Enhancements

### Planned Features

1. **Multi-Objective Optimization**
   - Pareto frontier analysis
   - Interactive trade-off exploration

2. **Machine Learning Integration**
   - Learn optimal weights from historical decisions
   - Personalized ranking based on user preferences

3. **Sensitivity Analysis**
   - Automatic robustness testing
   - Identify ranking stability

4. **Real-time Ranking**
   - API endpoint for on-demand ranking
   - Caching for frequently requested combinations

5. **Visualization**
   - Interactive ranking dashboard
   - Score breakdown charts
   - Constraint impact analysis

---

## References

- [EcoPackAI Project Documentation](../README.md)
- [Feature Engineering Guide](./feature_engineering.md)
- [Model Training Documentation](./model_training.md)
- [API Integration Guide](./api_integration.md)

---

## Contact & Support

For questions or issues related to material ranking:
- **Team**: EcoPackAI Development Team
- **Last Updated**: 2026-01-02
- **Version**: 1.0.0
