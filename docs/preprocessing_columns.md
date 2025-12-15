\# Preprocessing Column Definitions



This document defines the column groups used in the preprocessing pipeline

for the EcoPackAI materials dataset.



The grouping is frozen to ensure consistent preprocessing during

training, evaluation, and inference.



---



\## 1. Numeric Features



These features are continuous-valued material attributes.

They require missing value handling and scaling.



Applied transformations:

\- Median imputation

\- Standardization (StandardScaler)



\### Numeric Columns

\- CO2 Emission per kg (estimated)

\- Recyclability (%)

\- Recycled Content (%)

\- Reusability (%)

\- Biodegradation Time (days)

\- Load Handling Score

\- Moisture Resistance Score

\- Thermal Resistance Score

\- Cost per Unit (USD)



---



\## 2. Binary / Encoded Features



These features are already one-hot encoded (0/1) and are model-ready.

No scaling or imputation is applied.



Applied transformations:

\- Passthrough (no modification)



\### Binary Columns



\#### Material Type

\- Material Type\_Cardboard

\- Material Type\_Paper/Bio-Based

\- Material Type\_Plastic

\- Material Type\_Steel



\#### Packaging Type

\- Packaging Type\_Bubble Wrap (Minimal Use)

\- Packaging Type\_Cardboard Boxes

\- Packaging Type\_Foldable \& Stackable Containers

\- Packaging Type\_Plastic Totes \& Pallets

\- Packaging Type\_Protective Fillers (Paper/Biodegradable)

\- Packaging Type\_Steel Racks \& Containers



\#### Supplier Region

\- Supplier Region\_AMERICAS

\- Supplier Region\_APAC

\- Supplier Region\_EMEA

\- Supplier Region\_EU

\- Supplier Region\_LATAM

\- Supplier Region\_ROW



---



\## 3. Excluded Columns



The following columns are excluded from preprocessing and modeling to

avoid data leakage or because they serve only as identifiers.



\- Unnamed: 0

\- Material ID

\- recommended\_material\_type (target variable)

\- Final\_Recommendation\_Score



---



\## Notes

\- No categorical encoding is required at this stage since all categorical

&nbsp; variables are already encoded.

\- Product-level features are maintained in a separate dataset and will be

&nbsp; integrated in future iterations once a common join key is finalized.



