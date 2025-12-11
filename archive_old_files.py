import os
import shutil

os.makedirs("data/archive", exist_ok=True)

files_to_archive = [
    "data/processed/materials_with_co2_index.csv",
    "data/cleaned_datasets/materials_cleaned.csv"
]

for file in files_to_archive:
    if os.path.exists(file):
        shutil.copy(file, "data/archive/")
        print(f"Archived: {file}")

print("✅ Archiving completed!")
