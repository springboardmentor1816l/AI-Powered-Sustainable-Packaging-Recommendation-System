## Material Ranking Logic

### Objective
Rank candidate materials per product by combining predicted cost,
predicted CO₂ emissions, material suitability, and supplier compliance.

### Inputs
- Integrated dataset with model predictions
- Predicted cost (RF)
- Predicted CO₂ (XGBoost)

### Material Suitability Score
Computed from:
- Load handling
- Moisture resistance
- Thermal resistance
- Fragility compatibility

All components are normalized and equally weighted.

### Normalization
Metrics are min–max normalized **per product** to ensure fair comparison.

### Ranking Modes
- Sustainability-first
- Cost-first
- Balanced

Weights and constraints are configurable via YAML.

### Constraints (defaults)
- Minimum recyclability: 30%
- Minimum supplier compliance: 50%
- Cost capped at 95th percentile

### Output
A ranked list of materials per product with final composite scores.
