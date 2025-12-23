# Engineered Dataset Preview – EcoPackAI

## Overview
This document provides a preview of the dataset after applying feature
engineering logic. The engineered features enhance raw material data
with sustainability, cost efficiency, and suitability metrics.

The preview is illustrative and represents the structure of the dataset
after feature engineering integration.

---

## Original Attributes (Sample)
| material_id | material_type | cost_per_kg | recyclability_percent | strength |
|------------|---------------|-------------|------------------------|----------|
| MAT_001 | Cardboard | 0.28 | 98 | 6.0 |
| MAT_002 | Bioplastic | 0.45 | 75 | 5.5 |

---

## Engineered Features Added
| CO2_Impact_Index | Cost_Efficiency_Index | Material_Suitability_Score |
|-----------------|-----------------------|----------------------------|
| 82 | 88 | 79 |
| 70 | 72 | 84 |

---

## Integrated Dataset Structure (Preview)
| material_id | material_type | cost_per_kg | recyclability_percent | strength | CO2_Impact_Index | Cost_Efficiency_Index | Material_Suitability_Score |
|------------|---------------|-------------|------------------------|----------|------------------|-----------------------|----------------------------|
| MAT_001 | Cardboard | 0.28 | 98 | 6.0 | 82 | 88 | 79 |
| MAT_002 | Bioplastic | 0.45 | 75 | 5.5 | 70 | 72 | 84 |

---

## Notes
- Engineered features are scaled between 0–100.
- Higher values indicate better sustainability, efficiency, or suitability.
- Original raw attributes are retained for traceability.
- The enriched dataset will be used for ML training and recommendation scoring.

---

## Conclusion
The engineered dataset structure enables advanced analytics, ranking,
and AI-driven material recommendations in EcoPackAI.
