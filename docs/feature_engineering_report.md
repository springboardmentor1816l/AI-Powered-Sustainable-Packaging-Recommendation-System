
# Feature Engineering Report
---
## Objective
Derive critical composite metrics required for the EcoPackAI ML model.

## Formulas Used

1. **CO2_Impact_Index (Target/Feature - Lower is Better)**
   * **Purpose:** Measures overall environmental burden.
   * **Formula:** ((1.0 * Carbon Footprint) + (0.5 * Biodegradation Time)) / (0.01 * Recyclability %)
   * **Justification:** Normalizes the high penalty terms (CO2 and time) against the primary green factor (Recyclability).

2. **Cost_Efficiency_Index (Target/Feature - Lower is Better)**
   * **Purpose:** Measures cost effectiveness relative to protective performance.
   * **Formula:** Cost per Unit (USD) / (Load Score + Moisture Score + Thermal Score)
   * **Justification:** Provides a measure of performance per dollar spent.

3. **Material_Suitability_Score (Feature - Higher is Better)**
   * **Purpose:** General overall performance metric.
   * **Formula:** (Load Score + Moisture Score + Thermal Score) - (0.1 * Total Material Weight (tons))
   * **Justification:** Performance scores are positive; large weight is a penalty, making the score a comprehensive quality indicator.
