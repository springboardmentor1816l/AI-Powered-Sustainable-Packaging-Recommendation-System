import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------
# Load model
# -------------------------------
rf = joblib.load("ml/models/rf_cost.joblib")

# -------------------------------
# Load the SAME data pipeline used in training
# -------------------------------
X_train = pd.read_parquet("data/model_ready/X_train.parquet")
X_test  = pd.read_parquet("data/model_ready/X_test.parquet")

# Rebuild features exactly like training
X_train = pd.get_dummies(X_train)
X_test  = pd.get_dummies(X_test)

X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

# Safety: force numeric
X_test = X_test.apply(pd.to_numeric, errors="coerce").fillna(0)

# -------------------------------
# SHAP Explainability
# -------------------------------
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test)

# -------------------------------
# Output folder
# -------------------------------
out_dir = Path("outputs/explainability")
out_dir.mkdir(parents=True, exist_ok=True)

# Summary plot
plt.figure()
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig(out_dir / "shap_summary.png", bbox_inches="tight")
plt.close()

# Feature importance plot
importance = abs(shap_values).mean(axis=0)
imp_df = pd.DataFrame({"feature": X_test.columns, "importance": importance})
imp_df = imp_df.sort_values("importance", ascending=False)

plt.figure(figsize=(10, 6))
imp_df.head(15).plot.barh(x="feature", y="importance", legend=False)
plt.gca().invert_yaxis()
plt.title("Top Feature Importances")
plt.savefig(out_dir / "feature_importance.png", bbox_inches="tight")
plt.close()

print("✅ Explainability complete — plots saved in outputs/explainability/")
