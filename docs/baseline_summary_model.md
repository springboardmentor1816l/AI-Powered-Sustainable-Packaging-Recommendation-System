\# Baseline Model Summary – EcoPackAI

Date: Dec 18, 2025  

Author: Bhavana (Data Engineering + Data Science)



---



\## 🎯 Objective

To establish performance benchmarks for EcoPackAI using simple, interpretable baseline models before moving into advanced ML and optimization workflows.



These baselines allow the team to:



\- Validate dataset quality  

\- Confirm feature → target relationships  

\- Detect data leakage or feature dominance issues  

\- Benchmark future model performance  



---



\## 📌 Models Used



\### 1️⃣ Linear Regression (Cost Prediction)

\- Input Features: Full integrated feature matrix  

\- Target Variable: `cost\_per\_unit`  

\- Hyperparameters: Default  

\- Reason:

&nbsp; - Provides an interpretable linear relationship  

&nbsp; - Acts as a minimum performance baseline  

&nbsp; - Faster to train and evaluate



\### 2️⃣ Decision Tree Regressor (CO₂ Emission Prediction)

\- Input Features: Full integrated feature matrix  

\- Target Variable: `co2\_emission`  

\- Hyperparameters: Default  

\- Reason:

&nbsp; - Captures nonlinear feature interactions  

&nbsp; - Good beginner benchmark for sustainability metrics  

&nbsp; - Easy to visualize + explain



---



\## 📈 Dataset

Train/Test Split: 80/20  

Cross-Validation: K-Fold (5 folds, shuffled, seed=42)  

Task Targets:

\- Cost regression

\- CO₂ emission regression



---



\## 🧠 Key Findings

\- Both baseline models achieved \*\*extremely high accuracy\*\*.

\- R² scores are ≈ 1.0 on both test data and CV folds.

\- This indicates:

&nbsp; - Strong signal in features

&nbsp; - Minimal noise

&nbsp; - Good feature engineering

&nbsp; - No missing-value distortion



---



\## ⚠️ Notes / Caveats

\- Scores are so high that overfitting checks are required.

\- Future models should try:

&nbsp; - Regularized regression

&nbsp; - Ensemble trees  

&nbsp; - Neural networks  

\- SHAP explainability recommended to validate model behavior.



---



\## 🚀 Conclusion

Baseline model performance is outstanding and confirms:



EcoPackAI dataset is fully ready for serious ML pipelines.

This baseline will be the benchmark that future models MUST beat.



