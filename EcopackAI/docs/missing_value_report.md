# Missing Value Report — EcoPackAI

## Dataset
- Input: `EcopackAI\data\raw_datasets\materials\materials_raw.csv`
- Output: `EcopackAI\data\processed\cleaned_integrated_materials.csv`

## Missing Value Summary (Top Columns)
| column                          |   missing_count |   missing_percent |
|:--------------------------------|----------------:|------------------:|
| Waste Reduction Impact (%)      |               1 |          0.247525 |
| Carbon Footprint (kg CO2/unit)  |               1 |          0.247525 |
| CO2 Emission per kg (estimated) |               1 |          0.247525 |
| End-of-Life Disposal (%)        |               1 |          0.247525 |
| Biodegradation Time (days)      |               1 |          0.247525 |
| Reusability (%)                 |               1 |          0.247525 |
| Recycled Content (%)            |               1 |          0.247525 |
| Cost per Unit (USD)             |               1 |          0.247525 |
| Load Handling Score             |               1 |          0.247525 |
| Moisture Resistance Score       |               1 |          0.247525 |

## Strategy Used
- Numeric columns: **Median imputation**
- Categorical columns: **Most frequent (mode) imputation**
- Empty categorical values replaced with: `Unknown`

## Validation
- Remaining missing values after cleaning: **0**
