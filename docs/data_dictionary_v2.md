
# EcoPackAI Final Data Dictionary (v2)

This document provides comprehensive metadata for the final, ML-ready materials dataset, which has undergone cleaning, feature engineering, and MinMax scaling.

## Dataset-Level Summary

| Metric | Value |
| :--- | :--- |
| **Project** | EcoPackAI - AI-Powered Sustainable Packaging Recommendation System |
| **Status** | ML-Ready (Post-Scaling, Post-Encoding) |
| **Source** | Integrated Materials Data (Cross-joined with Products for Training) |
| **Number of Rows** | 404 |
| **Number of Columns** | 48 |
| **Primary Target Variables** | CO2_Impact_Index, Cost_Efficiency_Index |
| **Feature Groups** | Raw/Scaled Inputs, Engineered Indices, Categorical Encoded Features (OHE) |

## Column-Level Details

| Column Name | Data Type   | Description | Range / Categories   | Example Value   | Nullable   | Derived?   | Used in ML?   | Feature Group  |
|:---------------------------------------|:------------|:----------------------------------------------------------------------------------------------------------------|:---------------------|:----------------|:-----------|:-----------|:--------------|:--------------------|
| Material ID                            | object      | Unique identifier for the material.                                                                             | N/A                  | MAT_0001        | No         | No         | No            | Reference           |
| Recyclability (%)                      | float64     | Material�s reuse potential (Scaled value).                                                                      | [0.0, 1.0]           | 0.956           | No         | No         | Yes           | Raw/Scaled          |
| Recycled Content (%)                   | float64     | Percentage of recycled material used (Scaled).                                                                  | [0.0, 1.0]           | 0.794           | No         | No         | Yes           | Raw/Scaled          |
| Cost per Unit (USD)                    | float64     | Price metric for material (Scaled). Used as a basis for Cost Efficiency Index.                                  | [0.0, 1.0]           | 0.078           | No         | No         | Yes           | Raw/Scaled          |
| Carbon Footprint (kg CO2/unit)         | float64     | Material�s carbon footprint index (Scaled). Used as a basis for CO2 Impact Index.                               | [0.0, 1.0]           | 0.139           | No         | No         | Yes           | Raw/Scaled          |
| Load Handling Score                    | float64     | Mechanical strength capacity score (Scaled).                                                                    | [0.0, 1.0]           | 0.555           | No         | No         | Yes           | Raw/Scaled          |
| Total Material Weight (tons)           | float64     | Total material weight (Scaled). Used as penalty in Suitability Score.                                           | [0.0, 1.0]           | 0.130           | No         | No         | Yes           | Raw/Scaled          |
| CO2_Impact_Index                       | float64     | Composite score measuring environmental burden (Lower is better). **ML Target Variable.**                       | [0.0, 1.0]           | 0.198           | No         | Yes        | Yes           | Engineered          |
| Cost_Efficiency_Index                  | float64     | Composite score measuring cost-effectiveness relative to performance (Lower is better). **ML Target Variable.** | [0.0, 1.0]           | 0.245           | No         | Yes        | Yes           | Engineered          |
| Material_Suitability_Score             | float64     | Composite score for overall material quality (Higher is better). **ML Feature.**                                | [0.0, 1.0]           | 0.781           | No         | Yes        | Yes           | Engineered          |
| Material Type_Cardboard                | float64     | One-Hot Encoded feature. 1 if Material Type is Cardboard, 0 otherwise.                                          | {0, 1}               | 1.0             | No         | Yes        | Yes           | Categorical Encoded |
| Supplier Region_EMEA                   | float64     | One-Hot Encoded feature for supplier region (Europe, Middle East, Africa).                                      | {0, 1}               | 0.0             | No         | Yes        | Yes           | Categorical Encoded |
| Packaging Type_Plastic Totes & Pallets | float64     | One-Hot Encoded feature for packaging use type.                                                                 | {0, 1}               | 0.0             | No         | Yes        | Yes           | Categorical Encoded |