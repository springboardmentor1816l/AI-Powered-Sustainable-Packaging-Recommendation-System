import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


# Load Dataset

data = pd.read_csv("data/raw/product_dataset.csv")


# Define Column Groups

numeric_features = [
    "Product_Weight",
    "Fragility_Score",
    "Moisture_Sensitivity",
    "Thermal_Sensitivity",
    "CO2_Emission_per_kg",
    "Cost_per_Unit",
    "Load_Handling_Score",
    "CO2_Impact_Index",
    "Cost_Efficiency_Index"
]

categorical_features = [
    "Product_Category",
    "Material_Type",
    "Packaging_Type",
    "Recyclability_Category",
    "Supplier_Region"
]

binary_features = [
    "Hazardous_Material_Flag"
]

# Define Transformers

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

binary_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent"))
])

# Column Transformer

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
        ("bin", binary_transformer, binary_features)
    ],
    remainder="drop"
)


X = data[numeric_features + categorical_features + binary_features]

X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

preprocessor.fit(X_train)

os.makedirs("models/preprocessing", exist_ok=True)
joblib.dump(preprocessor, "models/preprocessing/preprocessing_pipeline.pkl")

X_transformed = preprocessor.transform(X_train)

sample_transformed = pd.DataFrame(
    X_transformed.toarray() if hasattr(X_transformed, "toarray") else X_transformed
)

os.makedirs("data/model_ready", exist_ok=True)
sample_transformed.head(50).to_csv(
    "data/model_ready/sample_transformed.csv",
    index=False
)

print("✅ Preprocessing pipeline built and saved successfully")
