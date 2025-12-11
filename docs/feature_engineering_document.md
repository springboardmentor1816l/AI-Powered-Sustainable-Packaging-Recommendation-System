
# Feature Engineering Document — EcoPackAI

## Overview
Computed features: CO2 Impact Index (CII), Cost Efficiency Index (CEI), Material Suitability Score (MSS).

## CO2 Impact Index (CII)
Formula:
- Normalize CO2_per_kg to 0..1 (co2_norm)
- Normalize biodegradation (log scale) to 0..1 (bio_norm)
- Map recyclability A->0,B->0.33,C->0.66,D->1 -> recy_score
- Material type score: domain mapping (bio-based=0, plastic=0.7, etc.)
- Weighted sum: cii = 0.5*co2_norm + 0.25*bio_norm + 0.2*recy_score + 0.05*mtype_score
- Scale: CII = cii * 100 (0 best, 100 worst)

## Cost Efficiency Index (CEI)
Formula:
- cost_per_unit = Cost_per_kg * Weight_per_unit_kg
- cost_norm = (cost_per_unit - min) / (max - min)
- cost_eff = 1 - cost_norm   (higher is better)
- durability normalized to 0..1
- recyclability bonus: A:+0.1, B:+0.06, C:+0.03, D:+0.0
- Weighted sum: cei = 0.6*cost_eff + 0.3*durability + 0.1*recy_bonus
- Scale: CEI = cei * 100 (higher better)

## Material Suitability Score (MSS)
Formula:
- Normalize material attributes: load_handling, moisture_resistance, thermal_resistance, durability to 0..1
- Weighted match: mss = 0.3*load + 0.25*moisture + 0.25*thermal + 0.2*durability
- Mandatory thresholds may apply (heavy penalty if fail)
- Scale: MSS = mss * 100 (higher better)

## Weights & assumptions
- Default weights shown in code. Adjust according to domain / stakeholder guidance.
- Missing inputs: medians or default constants used.
- Units: weight expected in grams (converted to kg by code). Cost in currency per kg.

