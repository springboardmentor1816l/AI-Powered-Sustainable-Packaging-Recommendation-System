import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_squared_error

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_csv("data/integrated_dataset_final_pdf.csv")
print("✅ Dataset loaded:", df.shape)

# -------------------------------------------------
# DROP INVALID / LEAKAGE COLUMNS
# -------------------------------------------------
DROP_COLS = [
    "product_id",
    "product_name",
    "material_id",
    "fragility_level",               # ❌ all NaN
    "cost_per_unit",                 # leakage
    "sustainability_score_final"     # composite
]

df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

# -------------------------------------------------
# TARGET
# -------------------------------------------------
TARGET = "co2_emission_score"

X = df.drop(columns=[TARGET])
y = df[TARGET]

# -------------------------------------------------
# ENCODE CATEGORICAL FEATURES
# -------------------------------------------------
for col in X.select_dtypes(include="object").columns:
    X[col] = LabelEncoder().fit_transform(X[col].astype(str))

# -------------------------------------------------
# TRAIN / TEST SPLIT
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42
)

# -------------------------------------------------
# BASELINE MODELS
# -------------------------------------------------
lr = LinearRegression()
dt = DecisionTreeRegressor(
    max_depth=5,
    min_samples_leaf=200,
    random_state=42
)

lr.fit(X_train, y_train)
dt.fit(X_train, y_train)

# -------------------------------------------------
# EVALUATION
# -------------------------------------------------
lr_pred = lr.predict(X_test)
dt_pred = dt.predict(X_test)

print("\n📊 CO₂ BASELINE RESULTS")

print("\nLinear Regression:")
print("R² Score :", r2_score(y_test, lr_pred))
print("RMSE     :", np.sqrt(mean_squared_error(y_test, lr_pred)))

print("\nDecision Tree (Regularized):")
print("R² Score :", r2_score(y_test, dt_pred))
print("RMSE     :", np.sqrt(mean_squared_error(y_test, dt_pred)))
