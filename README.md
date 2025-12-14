EcoPackAI – Exploratory Data Analysis (EDA)

This repository contains the Exploratory Data Analysis performed on the EcoPackAI_dataset.csv file.

### ✔ 1. EDA.ipynb  
Contains:
- Data loading  
- Structure overview  
- Summary statistics  
- Missing value detection  
- Duplicate check  
- Outlier analysis  
- Visualizations  
- Findings summary  

### ✔ 2. EcoPackAI_dataset.csv  
Single combined dataset with 404 rows & 23 columns.

### ✔ 3. missing_value_table.csv  
CSV generated during EDA containing missing count and % for each column.

### ✔ 4. data_quality_report.md  
A detailed report covering:
- Missing values  
- Duplicates  
- Outliers  
- Invalid entries  
- Cleaning recommendations  

##  Tools Used
- Python  
- Pandas  
- NumPy  
- Seaborn  
- Matplotlib  
- colab Notebook  

## Summary
The dataset was analyzed for completeness, consistency, and data quality.  
Overall quality is excellent with only 3 missing values and no duplicates.





# Dataset Preparation – Define Targets & Features

## Module
Data Preparation – (Model Development)

## Objective
To identify the target variable and finalize model features, and
prepare a clean dataset for the next stage of machine learning
(encoding and feature engineering).

## Dataset
Source file used:
- cleaned_integrated_materials.csv

## Target Variable
- material_type  
Represents the recommended sustainable packaging material.

## Features
All remaining columns after excluding the target variable were
used as model features. These include material properties,
cost-related attributes, and sustainability indicators.

## Files Generated
- dataset_prep.ipynb – Dataset preparation notebook
- X_raw.csv – Feature dataset
- y_raw.csv – Target dataset

## Notes
Column names were standardized to ensure consistency and avoid
errors during feature selection. The dataset is now ready for
encoding and model development.


