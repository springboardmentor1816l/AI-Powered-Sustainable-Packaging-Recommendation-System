summary = """
Random Forest Cost Prediction Model

Target Variable:
- Cost per unit (INR)

Model:
- Random Forest Regressor
- Number of trees: 100

Evaluation Metrics:
- Mean Absolute Error (MAE): 0.2226
- Root Mean Squared Error (RMSE): 0.3526
- R2 Score: 0.9972

Conclusion:
The Random Forest model demonstrates excellent performance with
low prediction error and a very high R2 score. The results indicate
that the model effectively captures the relationship between product
and material features and packaging cost. This trained model can be
integrated into the EcoPackAI system for cost-aware and sustainable
packaging recommendation workflows.
"""

with open("rf_cost_training_summary.md", "w") as f:
    f.write(summary)
