
# Products Encoding and Normalization Report (New Dataset)
---

## Encoding Strategy
1. **Nominal Categories** (category, shipping_type): Used **One-Hot Encoding** (OHE).

## Normalization Strategy
1. **Numeric Features** (product_weight_kg, fragility_index): Used **MinMaxScaler** to scale all features to the range [0, 1].
