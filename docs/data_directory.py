import pandas as pd
import os

# Ensure docs directory exists
os.makedirs("docs", exist_ok=True)

# Data Dictionary content
data = [
    ["material_id", "VARCHAR", "Unique material identifier", "No", "No", "Yes", "MAT_001"],
    ["material_type", "VARCHAR", "Type of packaging material", "No", "No", "Yes", "Cardboard"],
    ["strength_mpa", "FLOAT", "Material strength score", "No", "No", "Yes", "6.5"],
    ["weight_capacity", "FLOAT", "Maximum load capacity", "No", "No", "Yes", "5.2"],
    ["co2_emission_score", "FLOAT", "CO₂ emission per kg", "No", "No", "Yes", "0.54"],
    ["biodegradability_percent", "FLOAT", "Biodegradability percentage", "No", "No", "Yes", "85"],
    ["recyclability_percent", "FLOAT", "Recyclability percentage", "No", "No", "Yes", "98"],
    ["cost_per_kg", "FLOAT", "Cost per kg of material", "No", "No", "Yes", "0.28"],
    ["indusrty_use_case", "TEXT", "Intended industry use", "Yes", "No", "No", "E-commerce"],
    ["CO2_Impact_Index", "FLOAT", "Environmental sustainability score", "No", "Yes", "Yes", "82"],
    ["Cost_Efficiency_Index", "FLOAT", "Cost efficiency score", "No", "Yes", "Yes", "88"],
    ["Material_Suitability_Score", "FLOAT", "Material suitability score", "No", "Yes", "Yes", "79"]
]

# Create DataFrame
columns = [
    "Column Name",
    "Data Type",
    "Description",
    "Nullable",
    "Derived",
    "Used in ML",
    "Example"
]

df_dict = pd.DataFrame(data, columns=columns)

# Save to Excel
output_path = "data_dictionary_v2.xlsx"
df_dict.to_excel(output_path, index=False)

print("✅ data_dictionary_v2.xlsx created successfully at:", output_path)
