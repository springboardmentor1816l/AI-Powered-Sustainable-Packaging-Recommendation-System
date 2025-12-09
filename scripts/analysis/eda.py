import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------
#  SETUP
# ----------------------------
sns.set(style="whitegrid")

# Create output folders if not exist
os.makedirs("reports", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# ----------------------------
#  LOAD DATASET
# ----------------------------

print("📥 Loading dataset...")
df = pd.read_csv("ecopack_ai.csv")  # adjust path if needed

print("\nDataset loaded successfully!")
print(df.head())


# ----------------------------
#  BASIC STRUCTURE
# ----------------------------
print("\n📌 Dataset Shape (rows, columns):")
print(df.shape)

print("\n📌 Column Names:")
print(df.columns)

print("\n📌 Data Types:")
print(df.dtypes)


# ----------------------------
#  SUMMARY STATISTICS
# ----------------------------

print("\n📊 Summary Statistics (Numerical):")
print(df.describe())

print("\n📊 Unique Values Per Column:")
print(df.nunique())


# ----------------------------
#  MISSING VALUE ANALYSIS
# ----------------------------

print("\n🔍 Checking Missing Values...")
missing_values = df.isna().sum()
print(missing_values)

# Save missing values report
missing_values.to_csv("reports/missing_values_report.csv")
print("✔ Missing values report saved to reports/missing_values_report.csv")


# ----------------------------
#  DUPLICATE CHECK
# ----------------------------

duplicates = df.duplicated().sum()
print(f"\n🔍 Duplicate Rows Found: {duplicates}")


# ----------------------------
#  OUTLIER DETECTION (IQR METHOD)
# ----------------------------

print("\n📌 Detecting Outliers...")

numeric_cols = df.select_dtypes(include=[np.number]).columns
outlier_report = {}

def detect_outliers(column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower) | (df[column] > upper)]
    return len(outliers)

for col in numeric_cols:
    outlier_count = detect_outliers(col)
    outlier_report[col] = outlier_count

print("\n📊 Outlier Counts Per Column:")
print(outlier_report)

pd.Series(outlier_report).to_csv("reports/outlier_report.csv")
print("✔ Outlier report saved to reports/outlier_report.csv")


# ----------------------------
#  INVALID RANGE CHECKS
# ----------------------------

invalid_report = {}

def check_invalid(col, condition):
    return df[condition].shape[0]

if "recyclability_percent" in df.columns:
    invalid_report["recyclability_percent > 100"] = check_invalid(
        "recyclability_percent", df["recyclability_percent"] > 100
    )

if "biodegradability_percent" in df.columns:
    invalid_report["biodegradability_percent > 100"] = check_invalid(
        "biodegradability_percent", df["biodegradability_percent"] > 100
    )

if "cost_per_kg" in df.columns:
    invalid_report["cost_per_kg < 0"] = check_invalid(
        "cost_per_kg", df["cost_per_kg"] < 0
    )

print("\n⚠ Invalid Value Summary:")
print(invalid_report)

pd.Series(invalid_report).to_csv("reports/invalid_values_report.csv")
print("✔ Invalid value report saved.")


# ----------------------------
#  VISUALIZATIONS
# ----------------------------

print("\n📊 Generating Plots...")

# Histogram
df.hist(figsize=(12, 10), bins=30)
plt.tight_layout()
plt.savefig("plots/histograms.png")
plt.close()

# Boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df[numeric_cols])
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("plots/boxplots.png")
plt.close()

# Correlation Heatmap
# Correlation Heatmap (numeric columns only)
numeric_df = df.select_dtypes(include=[np.number])

print("\n📌 Numeric columns detected:", numeric_df.columns.tolist())

if numeric_df.shape[1] > 1:
    plt.figure(figsize=(10, 7))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
    plt.tight_layout()
    plt.savefig("plots/correlation_heatmap.png")
    plt.close()
    print("✔ Correlation heatmap saved.")
else:
    print("⚠ Not enough numeric columns for correlation heatmap.")



# ----------------------------
#  FINAL SUMMARY
# ----------------------------

print("\n🎉 EDA Completed Successfully!")
print("Generated Reports:")
print(" - reports/missing_values_report.csv")
print(" - reports/outlier_report.csv")
print(" - reports/invalid_values_report.csv")
print("\nGenerated Plots:")
print(" - plots/histograms.png")
print(" - plots/boxplots.png")
print(" - plots/correlation_heatmap.png")
