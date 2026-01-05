# Model Explainability Report

## 1. Overview
This document presents the explainability analysis performed on the trained machine learning model used in the AI-Powered Sustainable Packaging Recommendation System. The objective is to interpret model predictions, validate feature influence, and ensure alignment with sustainability and business logic.

The analysis focuses on the final trained material suitability prediction model, which plays a key role in downstream material ranking and recommendation.

---

## 2. Model Selected for Explainability
- Model Type: Random Forest–based prediction model
- Purpose: Predict material suitability / cost-related outcomes
- Target Variable: Material suitability score / cost impact
- Data Used: Test dataset only (unseen during training)

The preprocessing pipeline used during training was reused to ensure consistency and prevent data leakage.

---

## 3. Explainability Techniques Used

### 3.1 SHAP (SHapley Additive Explanations)
SHAP was used to analyze both global and local feature contributions. This technique explains how each feature contributes positively or negatively to model predictions.

- Global explanations identify the most influential features overall.
- Local explanations show why a specific prediction was made.

### 3.2 Permutation Feature Importance
Permutation importance was applied as a model-agnostic validation technique. It measures how model performance changes when individual feature values are randomly shuffled.

This method was used to cross-validate SHAP-based findings.

---

## 4. Global Feature Importance (SHAP Summary)

The SHAP summary plot highlights the most influential features affecting model predictions.

Key observations:
- Features related to material type significantly influence predictions.
- Sustainability-related attributes such as recyclability and biodegradability have strong impact.
- Weight and usage-related features contribute meaningfully to the final output.

The global feature influence aligns well with domain expectations for sustainable packaging selection.

(Refer to: `outputs/explainability/shap_summary.png`)

---

## 5. Local Prediction Explanation

A local SHAP analysis was performed on a single test instance to understand feature-level contributions for an individual prediction.

Key insights:
- Certain material properties positively pushed the prediction toward higher suitability.
- Higher weight or less sustainable attributes contributed negatively.
- The balance of these feature effects resulted in the final predicted value.

This confirms that individual predictions are explainable and logically driven.

(Refer to: `outputs/explainability/local_shap_explanation.png`)

---

## 6. Permutation Feature Importance Results

Permutation importance analysis identified features that cause the greatest decrease in model performance when disrupted.

Findings:
- Material type and sustainability scores caused the highest performance drop when permuted.
- These results closely match the SHAP-based global importance ranking.
- No single feature dominated the model in an unrealistic or suspicious manner.

(Refer to: `outputs/explainability/feature_importance.png`)

---

## 7. Validation Checklist

The explainability analysis confirms that:
- Important features logically influence predictions
- No data leakage-related features dominate the model
- Feature importance aligns with sustainability and business knowledge
- Explanations are consistent and reproducible

---

## 8. Conclusion

The explainability analysis demonstrates that the model is transparent, interpretable, and reliable. The combination of SHAP and permutation importance provides strong confidence in the model’s decision-making process and supports its use in sustainable packaging recommendations.
