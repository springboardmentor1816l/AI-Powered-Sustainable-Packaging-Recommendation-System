import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===================================================================
# Utility: Create output directory
# ===================================================================
os.makedirs("eda_plots", exist_ok=True)

# ===================================================================
# 1. Load Datasets
# ===================================================================
print("\n====== LOADING DATA ======\n")

df_materials = pd.read_csv(
    "data/material_dataset.csv"
)

df_packages = pd.read_csv(
    "data/product_dataset.csv"
)

print("====== DATA LOADED SUCCESSFULLY ======\n")

# ===================================================================
# 2. Shape
# ===================================================================
print("====== MATERIALS DATASET SHAPE ======")
print(df_materials.shape, "\n")

print("====== PACKAGING PRODUCTS DATASET SHAPE ======")
print(df_packages.shape, "\n")

# ===================================================================
# 3. Column Names
# ===================================================================
print("====== COLUMN NAMES (Materials) ======")
print(df_materials.columns, "\n")

print("====== COLUMN NAMES (Products) ======")
print(df_packages.columns, "\n")

# ===================================================================
# 4. Data Types
# ===================================================================
print("====== DATA TYPES (Materials) ======")
print(df_materials.dtypes, "\n")

print("====== DATA TYPES (Products) ======")
print(df_packages.dtypes, "\n")

# ===================================================================
# 5. Sample Preview
# ===================================================================
print("====== SAMPLE DATA (Materials) ======")
print(df_materials.head(), "\n")

print("====== SAMPLE DATA (Products) ======")
print(df_packages.head(), "\n")

# ===================================================================
# 6. Summary Statistics
# ===================================================================
print("====== SUMMARY STATISTICS (Materials) ======")
print(df_materials.describe(include="all"), "\n")

print("====== SUMMARY STATISTICS (Products) ======")
print(df_packages.describe(include="all"), "\n")

# ===================================================================
# 7. Missing Values
# ===================================================================
print("====== MISSING VALUES — MATERIALS ======")
missing_materials = df_materials.isna().sum()
print(missing_materials, "\n")

print("====== MISSING VALUES — PRODUCTS ======")
missing_products = df_packages.isna().sum()
print(missing_products, "\n")

# Save missing values to CSV
missing_df = pd.DataFrame({
    "materials_missing": missing_materials,
    "products_missing": missing_products
})
missing_df.to_csv("missing_value_table.csv")

# ===================================================================
# 8. Duplicate Records
# ===================================================================
print("====== DUPLICATES ======")
print("Materials duplicates:", df_materials.duplicated().sum())
print("Products duplicates:", df_packages.duplicated().sum(), "\n")

# ===================================================================
# 9. Outlier Detection (IQR Method)
# ===================================================================
def detect_outliers(df, column):
    if df[column].dtype not in ["int64", "float64"]:
        return 0

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return ((df[column] < lower) | (df[column] > upper)).sum()

outliers_materials = {col: detect_outliers(df_materials, col) for col in df_materials.columns}
outliers_products = {col: detect_outliers(df_packages, col) for col in df_packages.columns}

print("====== OUTLIERS — MATERIALS ======")
print(outliers_materials, "\n")

print("====== OUTLIERS — PRODUCTS ======")
print(outliers_products, "\n")

# ===================================================================
# 10. Visualizations
# ===================================================================

print("====== GENERATING PLOTS ======\n")

# ---- Numeric Columns Only ----
numeric_materials = df_materials.select_dtypes(include=['int64', 'float64'])
numeric_packages = df_packages.select_dtypes(include=['int64', 'float64'])

# Histograms (Materials)
numeric_materials.hist(figsize=(12, 8))
plt.tight_layout()
plt.savefig("eda_plots/materials_hist.png")
plt.close()

# Histograms (Products)
numeric_packages.hist(figsize=(12, 8))
plt.tight_layout()
plt.savefig("eda_plots/products_hist.png")
plt.close()

# Correlation Heatmaps
plt.figure(figsize=(10, 6))
plt.imshow(numeric_materials.corr(), cmap="viridis")
plt.colorbar()
plt.title("Materials Correlation Heatmap")
plt.savefig("eda_plots/materials_corr_heatmap.png")
plt.close()

plt.figure(figsize=(10, 6))
plt.imshow(numeric_packages.corr(), cmap="viridis")
plt.colorbar()
plt.title("Products Correlation Heatmap")
plt.savefig("eda_plots/products_corr_heatmap.png")
plt.close()

print("====== PLOTS SAVED TO eda_plots/ ======\n")

# ===================================================================
# 11. Final Message
# ===================================================================
print("====== EDA COMPLETED SUCCESSFULLY 🎉 ======")
