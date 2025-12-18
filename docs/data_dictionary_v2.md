# Data Dictionary v2 – EcoPackAI

## Dataset Summary
- Cleaned rows: ~300+
- Engineered features: 3
- Model-ready features: 9
- Format: Parquet
- ML Ready: Yes

## Feature Groups
- Raw attributes
- Performance scores
- Sustainability metrics
- Engineered indices (CII, CEI, MSS)

---

## Column Definitions

### CII
- Type: Float
- Range: 0–100
- Description: CO₂ Impact Index
- Derived: Yes
- Used in ML: Yes

### CEI
- Type: Float
- Range: 0–100
- Description: Cost Efficiency Index
- Derived: Yes
- Used in ML: Yes

### MSS
- Type: Float
- Range: 0–100
- Description: Material Suitability Score
- Derived: Yes
- Used in ML: Yes

### moisture_resistance_score
- Type: Integer
- Range: 1–10
- Derived: No
- Used in ML: Yes

### thermal_resistance_score
- Type: Integer
- Range: 1–10
- Derived: No
- Used in ML: Yes
