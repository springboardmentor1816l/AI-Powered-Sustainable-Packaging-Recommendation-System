import pandas as pd

df = pd.read_csv('data/ml_ready/X_raw.csv')

print("="*60)
print("DATA STATISTICS")
print("="*60)

fields = {
    'material_suitability_score': 'Material Suitability',
    'supplier_sustainability_compliance_percent': 'Compliance',
    'load_handling_score': 'Load Handling',
    'moisture_resistance_score': 'Moisture Resistance',
    'thermal_resistance_score': 'Thermal Resistance'
}

for col, name in fields.items():
    if col in df.columns:
        print(f"\n{name}:")
        print(f"  Min: {df[col].min ():.2f}")
        print(f"  Max: {df[col].max():.2f}")
        print(f"  Mean: {df[col].mean():.2f}")
