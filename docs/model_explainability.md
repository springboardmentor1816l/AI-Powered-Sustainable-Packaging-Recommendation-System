Model Explainability – EcoPackAI
Overview

This document provides an interpretability analysis for the CO₂ prediction model in the EcoPackAI system. Explainability techniques, including SHAP (SHapley Additive exPlanations), were applied to understand feature influence on model predictions. These insights improve transparency, trust, and enable data-driven decision-making for material recommendations.

Dataset & Model

Model type: XGBoost Regressor

Target variable: co2_emission_per_kg

Number of features: 15

Sample used for explainability: 1000 rows (random subsample from full dataset)

SHAP Analysis

SHAP values were computed using XGBoost’s native pred_contribs=True method.
SHAP measures the contribution of each feature to a specific prediction, providing both global and local interpretability.

Global Feature Importance

The top influential features based on mean absolute SHAP values are:

Rank	Feature	Importance
1	material_type	High
2	product_weight	High
3	co2_emission_per_kg	High
4	recyclability_category	Medium
5	fragility_score	Medium
…	…	…

Interpretation:

material_type, product_weight, and co2_emission_per_kg dominate CO₂ predictions. This aligns with domain knowledge: heavier products and certain materials inherently emit more CO₂.

Features like recyclability_category influence sustainability-driven outcomes but have moderate contribution to CO₂ predictions.

Local Explanation (SHAP Summary Plot)

The SHAP summary plot (outputs/explainability/shap_summary.png) visually shows how each feature impacts predictions across the sample.

Features with red values increase CO₂ emissions, while blue values decrease it.

The spread of SHAP values indicates which features are consistently influential vs. those with context-dependent effects.

Feature Importance (Ranked by Influence)

The horizontal bar plot (outputs/explainability/feature_importance.png) ranks features by mean |SHAP value|, confirming the global influence order observed in the SHAP summary.

This plot helps stakeholders quickly identify critical drivers of CO₂ emissions.

Key Insights

Material type is the most significant predictor of CO₂ emissions, highlighting the importance of material selection for sustainable packaging.

Weight and CO₂ emission per kg are direct contributors and validate the model’s alignment with physical principles.

Recyclability and sustainability-related scores influence predictions moderately, suggesting potential for multi-objective optimization in recommendations.

No features related to cost or supplier region dominate unexpectedly, indicating no leakage and robust model behavior.

Recommendations for Stakeholders

Focus on low-emission materials for packaging, as material type and CO₂ intensity are primary drivers.

Monitor heavy products closely, since product weight significantly increases CO₂ predictions.

Use feature importance plots to justify material recommendations for business and sustainability teams.Model Explainability – EcoPackAI
Overview

This document provides an interpretability analysis for the CO₂ prediction model in the EcoPackAI system. Explainability techniques, including SHAP (SHapley Additive exPlanations), were applied to understand feature influence on model predictions. These insights improve transparency, trust, and enable data-driven decision-making for material recommendations.

Dataset & Model

Model type: XGBoost Regressor

Target variable: co2_emission_per_kg

Number of features: 15

Sample used for explainability: 1000 rows (random subsample from full dataset)

SHAP Analysis

SHAP values were computed using XGBoost’s native pred_contribs=True method.
SHAP measures the contribution of each feature to a specific prediction, providing both global and local interpretability.

Global Feature Importance

The top influential features based on mean absolute SHAP values are:

Rank	Feature	Importance
1	material_type	High
2	product_weight	High
3	co2_emission_per_kg	High
4	recyclability_category	Medium
5	fragility_score	Medium
…	…	…

Interpretation:

material_type, product_weight, and co2_emission_per_kg dominate CO₂ predictions. This aligns with domain knowledge: heavier products and certain materials inherently emit more CO₂.

Features like recyclability_category influence sustainability-driven outcomes but have moderate contribution to CO₂ predictions.

Local Explanation (SHAP Summary Plot)

The SHAP summary plot (outputs/explainability/shap_summary.png) visually shows how each feature impacts predictions across the sample.

Features with red values increase CO₂ emissions, while blue values decrease it.

The spread of SHAP values indicates which features are consistently influential vs. those with context-dependent effects.

Feature Importance (Ranked by Influence)

The horizontal bar plot (outputs/explainability/feature_importance.png) ranks features by mean |SHAP value|, confirming the global influence order observed in the SHAP summary.

This plot helps stakeholders quickly identify critical drivers of CO₂ emissions.

Key Insights

Material type is the most significant predictor of CO₂ emissions, highlighting the importance of material selection for sustainable packaging.

Weight and CO₂ emission per kg are direct contributors and validate the model’s alignment with physical principles.

Recyclability and sustainability-related scores influence predictions moderately, suggesting potential for multi-objective optimization in recommendations.

No features related to cost or supplier region dominate unexpectedly, indicating no leakage and robust model behavior.

Recommendations for Stakeholders

Focus on low-emission materials for packaging, as material type and CO₂ intensity are primary drivers.

Monitor heavy products closely, since product weight significantly increases CO₂ predictions.

Use feature importance plots to justify material recommendations for business and sustainability teams.