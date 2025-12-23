import pandas as pd

# Define the data structure
data = {
    "Column name": [],
    "Data type": [],
    "Description": [],
    "Range / Categories": [],
    "Example": [],
    "Nullable": [],
    "Derived": [],
    "Used in ML": []
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel file
file_path = r'C:/Users/Sneha/OneDrive/Desktop/EcoPackAI/docs/docs/data_dictionary.xlsx'
df.to_excel(file_path, index=False)