# Data Validation Report

## 1. Overview
The purpose of this report is to document issues found in the raw datasets
and summarize the cleaning steps performed.

## 2. Datasets Validated
- Materials dataset
- Products dataset
- Sustainability dataset

## 3. Validation Checks
- Column names standardized to snake_case
- Missing values identified and handled
- Removed duplicate records
- Datatype corrections applied (int, float, text, boolean)
- Outliers reviewed

## 4. Cleaning Summary
- Filled missing numerical values with mean/median
- Removed 2 duplicate rows
- Converted units where required
- Ensured consistent category labels

## 5. Output
Cleaned datasets saved at: `/data/processed/`
