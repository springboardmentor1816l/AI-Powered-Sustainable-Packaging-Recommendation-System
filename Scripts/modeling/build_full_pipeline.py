import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# Load training data
X = pd.read_parquet("data/model_ready/X_train.parquet")
y = pd.read_parquet("data/model_ready/y_train.parquet")["cost_per_kg"]

# Identify categorical & numeric columns
cat_cols = X.select_dtypes(include="object").columns
num_cols = X.select_dtypes(exclude="object").columns

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("num", "passthrough", num_cols)
])

model = RandomForestRegressor(n_estimators=300, random_state=42)

full_pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("model", model)
])

full_pipeline.fit(X, y)

joblib.dump(full_pipeline, "ml/models/rf_cost_pipeline.joblib")

print("✅ Full production pipeline saved")
