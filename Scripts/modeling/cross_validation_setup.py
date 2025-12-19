from sklearn.model_selection import KFold
import joblib
import os

# Ensure output folder exists
os.makedirs("models/cv", exist_ok=True)

# 5-Fold Cross Validation
cv = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# Save CV object
joblib.dump(
    cv,
    "models/cv/kfold_5.pkl"
)

print("Cross-validation strategy saved")
