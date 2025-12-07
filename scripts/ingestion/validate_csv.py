import pandas as pd

# Change the file path as needed
file_path = "data/raw_datasets/materials.csv"

df = pd.read_csv(file_path)

print("=== DATA INFO ===")
print(df.info())

print("\n=== NULL VALUES ===")
print(df.isnull().sum())

print("\n=== SAMPLE ROWS ===")
print(df.head())
