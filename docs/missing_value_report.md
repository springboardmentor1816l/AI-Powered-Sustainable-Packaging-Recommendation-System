# Missing Value Report

## Overview
This report describes how missing values were handled in the EcoPackAI dataset.

## Identification of Missing Values
Missing values were found in both numeric and categorical columns.

## Strategy Used
- Numeric columns were filled using the median value.
- Categorical columns were filled using the most frequent value (mode).
- Rows with more than 50% missing values were removed.

## Result
All missing values were handled successfully.
The cleaned dataset was saved as:
cleaned_integrated_materials.csv
