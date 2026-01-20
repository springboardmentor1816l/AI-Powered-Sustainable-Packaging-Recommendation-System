This document defines the feature engineering logic for EcoPackAI.
It covers the three main engineered indices used for sustainability scoring, pricing evaluation, and packaging-material suitability:

CO₂ Impact Index (CII)

Cost Efficiency Index (CEI)

Material Suitability Score (MSS)

All outputs are scaled between 0–1 for consistency and ML-readiness.
1. CO₂ Impact Index (CII)
Input Columns Used

Carbon Footprint (kg CO2/unit)

Biodegradation Time (days)

Recyclability Category (A/B/C/D)

Recyclability Mapping
Category	Score
A	1.00
B	0.75
C	0.50
D	0.25
Normalization Rules
Carbon Footprint Normalization

Higher CO₂ → worse → lower score

co2_norm = (CarbonFootprint - min) / (max - min)

Biodegradation Time Normalization

Lower biodegradation time → better

bio_score = 1 - (BiodegradationDays - min) / (max - min)
Final CII Formula (0–1)
CII = 0.40 * (1 - co2_norm)
    + 0.30 * bio_score
    + 0.30 * recyclability_score
2. Cost Efficiency Index (CEI)
Input Columns Used

Cost per Unit (USD)

Total Material Weight (tons) → converted to kg

Durability Rating

Recyclability Category

Feature Components
Cost Normalization

Lower cost → better

cost_norm = 1 - (CostPerUnit - min) / (max - min)

Durability Normalization
dur_norm = DurabilityRating / 10

Final CEI Formula (0–1)
CEI = 0.50 * cost_norm
    + 0.20 * recyclability_score
    + 0.30 * dur_norm

3. Material Suitability Score (MSS)

Input Columns Used

Load Handling Score

Moisture Resistance Score

Thermal Resistance Score

Durability Rating

Suitable Product Categories

Normalization Rules
load_norm        = normalize(LoadHandlingScore)
moisture_norm    = MoistureResistanceScore / 10
thermal_norm     = ThermalResistanceScore / 10
durability_norm  = DurabilityRating / 10

Category Bonus

Materials suitable for more categories are more versatile.

category_bonus = min((number_of_categories * 0.02), 0.10)

Final MSS Formula (0–1)
MSS = 0.25 * load_norm
    + 0.25 * moisture_norm
    + 0.20 * thermal_norm
    + 0.20 * durability_norm
    + 0.10 * category_bonus
