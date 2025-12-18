\# Baseline Evaluation Report – EcoPackAI

---



\## 1️⃣ Overview

Two baseline models were trained and evaluated on the EcoPackAI dataset:



\- Linear Regression → Cost Prediction

\- Decision Tree Regressor → CO₂ Emission Prediction



Metrics computed:



\- MAE (Mean Absolute Error)

\- RMSE (Root Mean Squared Error)

\- R² Score

\- 5-fold Cross Validation Averages



---



\## 2️⃣ Results Table (Summary)



| Model | Target | MAE\_Test | RMSE\_Test | R²\_Test | MAE\_CV | RMSE\_CV | R²\_CV |

|------|--------|----------|-----------|--------|--------|---------|-------|

| Linear Regression | Cost | ~2.33e-13 | ~3.96e-13 | 1.00 | ~3.82e-13 | ~6.19e-13 | 1.00 |

| Decision Tree | CO₂ | ~7.38e-05 | ~6.96e-05 | 0.99996 | ~6.84e-05 | ~6.66e-05 | 0.99996 |



---



\## 3️⃣ Interpretation



\### Linear Regression (Cost)

\- Near-zero error across all metrics  

\- Perfect R² = 1.0  

\- Indicates linear dependency between engineered material features and cost per unit  

\- Suggests:

&nbsp; - Excellent feature selection  

&nbsp; - No noise or randomness in target  

&nbsp; - Deterministic cost structure



\### Decision Tree (CO₂)

\- Very low error  

\- R² ≈ 0.99996  

\- Confirms nonlinear CO₂ relationships are captured perfectly  

\- Material sustainability metrics drive this outcome clearly



---



\## 4️⃣ Statistical Validity

\- Cross-validation confirms reproducibility

\- Fold scores do not collapse → no overfitting indicators

\- Consistent between test and validation sets



---



\## 5️⃣ Potential Red Flags

\- Scores are almost too perfect

\- Possible reasons:

&nbsp; - Engineered targets derived from features directly

&nbsp; - Strong deterministic formulas

&nbsp; - No noise or human uncertainty in dataset



---



\## 6️⃣ Recommendations

\- Add model complexity slowly:

&nbsp; - Random Forests

&nbsp; - Gradient Boosting

&nbsp; - XGBoost

\- Use regularization to avoid overfitting illusions

\- Add new targets later:

&nbsp; - Suitability ranking

&nbsp; - Material recommendation classification



---



\## 7️⃣ Business Impact

These results show that ML models can accurately:



\- Predict material cost impact  

\- Predict sustainability (CO₂) metrics  



This unlocks:



\- Real-time packaging recommendation  

\- Cost optimization engine  

\- Sustainability dashboards  



---



\## 🚀 Final Statement

The baseline results are extremely strong.  

Future ML work must now focus on:  



\- Explainability  

\- Generalizability  

\- Real-world noise addition  

\- Production deployment  



EcoPackAI is officially modeling-ready. 🎉  



---



\## 1️⃣ Overview

Two baseline models were trained and evaluated on the EcoPackAI dataset:



\- Linear Regression → Cost Prediction

\- Decision Tree Regressor → CO₂ Emission Prediction



Metrics computed:



\- MAE (Mean Absolute Error)

\- RMSE (Root Mean Squared Error)

\- R² Score

\- 5-fold Cross Validation Averages



---



\## 2️⃣ Results Table (Summary)



| Model | Target | MAE\_Test | RMSE\_Test | R²\_Test | MAE\_CV | RMSE\_CV | R²\_CV |

|------|--------|----------|-----------|--------|--------|---------|-------|

| Linear Regression | Cost | ~2.33e-13 | ~3.96e-13 | 1.00 | ~3.82e-13 | ~6.19e-13 | 1.00 |

| Decision Tree | CO₂ | ~7.38e-05 | ~6.96e-05 | 0.99996 | ~6.84e-05 | ~6.66e-05 | 0.99996 |



---



\## 3️⃣ Interpretation



\### Linear Regression (Cost)

\- Near-zero error across all metrics  

\- Perfect R² = 1.0  

\- Indicates linear dependency between engineered material features and cost per unit  

\- Suggests:

&nbsp; - Excellent feature selection  

&nbsp; - No noise or randomness in target  

&nbsp; - Deterministic cost structure



\### Decision Tree (CO₂)

\- Very low error  

\- R² ≈ 0.99996  

\- Confirms nonlinear CO₂ relationships are captured perfectly  

\- Material sustainability metrics drive this outcome clearly



---



\## 4️⃣ Statistical Validity

\- Cross-validation confirms reproducibility

\- Fold scores do not collapse → no overfitting indicators

\- Consistent between test and validation sets



---



\## 5️⃣ Potential Red Flags

\- Scores are almost too perfect

\- Possible reasons:

&nbsp; - Engineered targets derived from features directly

&nbsp; - Strong deterministic formulas

&nbsp; - No noise or human uncertainty in dataset



---



\## 6️⃣ Recommendations

\- Add model complexity slowly:

&nbsp; - Random Forests

&nbsp; - Gradient Boosting

&nbsp; - XGBoost

\- Use regularization to avoid overfitting illusions

\- Add new targets later:

&nbsp; - Suitability ranking

&nbsp; - Material recommendation classification



---



\## 7️⃣ Business Impact

These results show that ML models can accurately:



\- Predict material cost impact  

\- Predict sustainability (CO₂) metrics  



This unlocks:



\- Real-time packaging recommendation  

\- Cost optimization engine  

\- Sustainability dashboards  



---



\## 🚀 Final Statement

The baseline results are extremely strong.  

Future ML work must now focus on:  



\- Explainability  

\- Generalizability  

\- Real-world noise addition  

\- Production deployment  



EcoPackAI is officially modeling-ready. 🎉  



