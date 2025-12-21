import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

DATA_PATH = "data/interim/product_material_integrated.csv"
PIPELINE_PATH = "models/preprocessing/integrated_preprocessing_pipeline.pkl"

os.makedirs("models/preprocessing", exist_ok=True)

df = pd.read_csv(DATA_PATH)

TARGET = "Material Type"

NUMERIC_FEATURES = [
    "product_weight_kg",
    "fragility_index",
    "Recyclability (%)",
    "Recycled Content (%)",
    "Reusability (%)",
    "Biodegradation Time (days)",
    "End-of-Life Disposal (%)",
    "Carbon Footprint (kg CO2/unit)",
    "CO2 Emission per kg (estimated)",
    "Waste Reduction Impact (%)",
    "Sustainability Target Progress (%)",
    "Load Handling Score",
    "Moisture Resistance Score",
    "Thermal Resistance Score",
    "Cost per Unit (USD)",
    "Annual Usage (units)",
    "Total Material Weight (tons)",
    "Supplier Sustainability Compliance (%)"
]

CATEGORICAL_FEATURES = [
    "category",
    "shipping_type",
    "Packaging Type",
    "Supplier Region",
    "Recyclability Category"
]

X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
y = df[TARGET]

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, NUMERIC_FEATURES),
    ("cat", categorical_pipeline, CATEGORICAL_FEATURES)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

preprocessor.fit(X_train)

joblib.dump(preprocessor, PIPELINE_PATH)

print("✅ Integrated preprocessing pipeline built and saved successfully")
