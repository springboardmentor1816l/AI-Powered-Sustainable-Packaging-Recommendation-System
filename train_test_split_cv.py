import pandas as pd
import json
import os

from sklearn.model_selection import train_test_split, StratifiedKFold
# Load ML-ready dataset

data = pd.read_csv("data/raw/product_dataset.csv")
# Define Features & Target

feature_columns = [
    "Product_Weight",
    "Fragility_Score",
    "Moisture_Sensitivity",
    "Thermal_Sensitivity",
    "CO2_Emission_per_kg",
    "Cost_per_Unit",
    "Load_Handling_Score",
    "CO2_Impact_Index",
    "Cost_Efficiency_Index",
    "Product_Category",
    "Material_Type",
    "Packaging_Type",
    "Recyclability_Category",
    "Supplier_Region",
    "Hazardous_Material_Flag"
]

target_variables = [
    "Cost_per_Unit",
    "CO2_Emission_per_kg"
]

X = data[feature_columns]
y = data[target_variables]


# Train-Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=data["Product_Category"]
)


# Cross-Validation Strategy

cv_strategy = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# Save Metadata

metadata = {
    "dataset": "Integrated EcoPackAI Product-Material Dataset",
    "train_size": 0.8,
    "test_size": 0.2,
    "stratification_column": "Product_Category",
    "cross_validation": {
        "method": "StratifiedKFold",
        "n_splits": 5,
        "shuffle": True,
        "random_seed": 42
    },
    "features_used": feature_columns,
    "target_variables": target_variables
}

os.makedirs("ml/metadata", exist_ok=True)
with open("ml/metadata/split_metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("✅ Train-test split and cross-validation metadata saved successfully")
