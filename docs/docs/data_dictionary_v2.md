Final Data Dictionary – v2
Project: EcoPackAI

==================================================
DATASET-LEVEL SUMMARY
==================================================

Dataset Name: materials_model_ready
Total Rows: <put exact row count>
Total Columns: <put exact column count>

Feature Groups:
- Raw Features: Original material attributes
- Engineered Features: Sustainability and efficiency scores
- Scaled Features: Normalized numeric values
- Encoded Features: One-hot encoded categorical variables

==================================================
COLUMN-LEVEL DETAILS
==================================================

Column Name: strength_mpa
Data Type: Float
Description: Mechanical strength of material
Range / Allowed Values: > 0
Example Value: 45.6
Nullable: No
Derived: No
Used in ML: Yes

--------------------------------------------------

Column Name: weight_capacity
Data Type: Float
Description: Maximum load handling capacity
Range / Allowed Values: > 0
Example Value: 120.0
Nullable: No
Derived: No
Used in ML: Yes

--------------------------------------------------

Column Name: biodegradability_percent
Data Type: Float
Description: Percentage of material that is biodegradable
Range / Allowed Values: 0–100
Example Value: 85.0
Nullable: No
Derived: No
Used in ML: Yes

--------------------------------------------------

Column Name: co2_emission_score
Data Type: Float
Description: CO2 emission impact score
Range / Allowed Values: ≥ 0
Example Value: 2.3
Nullable: No
Derived: No
Used in ML: Yes

--------------------------------------------------

Column Name: recyclability_percent
Data Type: Float
Description: Percentage of material recyclable
Range / Allowed Values: 0–100
Example Value: 90.0
Nullable: No
Derived: No
Used in ML: Yes

--------------------------------------------------

Column Name: cost_per_kg
Data Type: Float
Description: Cost of material per kilogram
Range / Allowed Values: > 0
Example Value: 120.50
Nullable: No
Derived: No
Used in ML: Yes

--------------------------------------------------

Column Name: co2_impact_index
Data Type: Float
Description: Engineered sustainability score
Range / Allowed Values: 0–100
Example Value: 78.4
Nullable: No
Derived: Yes
Used in ML: Yes

--------------------------------------------------

Column Name: cost_efficiency_index
Data Type: Float
Description: Engineered cost efficiency score
Range / Allowed Values: 0–100
Example Value: 82.1
Nullable: No
Derived: Yes
Used in ML: Yes

--------------------------------------------------

Column Name: material_suitability_score
Data Type: Float
Description: Engineered suitability score
Range / Allowed Values: 0–100
Example Value: 88.9
Nullable: No
Derived: Yes
Used in ML: Yes

--------------------------------------------------

Column Name: material_type_<category>
Data Type: Binary (0/1)
Description: One-hot encoded material type
Range / Allowed Values: 0 or 1
Example Value: 1
Nullable: No
Derived: Yes
Used in ML: Yes

--------------------------------------------------

Column Name: industry_use_case_<category>
Data Type: Binary (0/1)
Description: One-hot encoded industry use case
Range / Allowed Values: 0 or 1
Example Value: 0
Nullable: No
Derived: Yes
Used in ML: Yes
