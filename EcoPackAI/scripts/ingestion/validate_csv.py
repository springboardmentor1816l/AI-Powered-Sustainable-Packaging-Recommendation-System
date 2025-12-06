import pandas as pd
import sys

# If no argument passed, use default file
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = "C:\\Users\\Tanmay\\AI-Powered-Sustainable-Packaging-Recommendation-System\\data\\material_dataset.csv"
print("Validating:", file_path)

df = pd.read_csv(file_path)

print("\n===== BASIC INFORMATION =====")
print(df.info())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATES =====")
print(df.duplicated().sum())

print("\n===== SAMPLE ROWS =====")
print(df.head())
