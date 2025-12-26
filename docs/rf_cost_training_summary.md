\# Random Forest Cost Prediction – Training Summary



\## Objective

Predict packaging cost per unit (INR) using integrated product and material features.



\## Model

Random Forest Regressor



features used:



&nbsp;   # --- Core product attributes ---

&nbsp;   "product\_weight\_kg",

&nbsp;   "fragility\_index",

&nbsp;   "shipping\_risk\_score",



&nbsp;   # --- Shipping type (one-hot already) ---

&nbsp;   "shipping\_type\_Air",

&nbsp;   "shipping\_type\_Road",

&nbsp;   "shipping\_type\_Sea",



&nbsp;   # --- Product category ---

&nbsp;   "category\_Cosmetics",

&nbsp;   "category\_Drinkware",

&nbsp;   "category\_Electronics",

&nbsp;   "category\_Food",

&nbsp;   "category\_Paper Product",

&nbsp;   "category\_Pharmacy",



&nbsp;   # --- Material \& sustainability properties ---

&nbsp;   "Recyclability (%)",

&nbsp;   "Recycled Content (%)",

&nbsp;   "Reusability (%)",

&nbsp;   "Biodegradation Time (days)",

&nbsp;   "End-of-Life Disposal (%)",

&nbsp;   "Waste Reduction Impact (%)",

&nbsp;   "Sustainability Target Progress (%)",



&nbsp;   # --- Mechanical \& protection scores ---

&nbsp;   "Load Handling Score",

&nbsp;   "Moisture Resistance Score",

&nbsp;   "Thermal Resistance Score",



&nbsp;   # --- Usage \& scale ---

&nbsp;   "Annual Usage (units)",

&nbsp;   "Total Material Weight (tons)",



&nbsp;   # --- Supplier attributes ---

&nbsp;   "Supplier Sustainability Compliance (%)",

&nbsp;   "Supplier Region\_AMERICAS",

&nbsp;   "Supplier Region\_APAC",

&nbsp;   "Supplier Region\_EMEA",

&nbsp;   "Supplier Region\_EU",

&nbsp;   "Supplier Region\_LATAM",

&nbsp;   "Supplier Region\_ROW",



&nbsp;   # --- Packaging type ---

&nbsp;   "Packaging Type\_Bubble Wrap (Minimal Use)",

&nbsp;   "Packaging Type\_Cardboard Boxes",

&nbsp;   "Packaging Type\_Foldable \& Stackable Containers",

&nbsp;   "Packaging Type\_Plastic Totes \& Pallets",

&nbsp;   "Packaging Type\_Protective Fillers (Paper/Biodegradable)",

&nbsp;   "Packaging Type\_Steel Racks \& Containers",



&nbsp;   # --- Material type ---

&nbsp;   "Material Type\_Cardboard",

&nbsp;   "Material Type\_Paper/Bio-Based",

&nbsp;   "Material Type\_Plastic",

&nbsp;   "Material Type\_Steel",



&nbsp;   # --- Suitability score (allowed) ---

&nbsp;   "MSS"



\## Target

Cost per Unit (INR)



\## Hyperparameters

\- n\_estimators: 300

\- max\_depth: 12

\- min\_samples\_split: 5

\- min\_samples\_leaf: 2

\- random\_state: 42



\## Training Strategy

\- Train-test split: 80/20

\- 5-fold cross-validation

\- Metric: MAE



\## Observations

Random Forest captured nonlinear relationships between material sustainability scores and cost more effectively than baseline linear models.



\## Limitations

\- Performance sensitive to noisy cost labels

\- Requires sufficient data for generalization



