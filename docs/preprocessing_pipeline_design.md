
# Preprocessing Pipeline Design Summary

## Objective
To create a robust, reusable pipeline that ensures consistency between the pre-processed training data and raw inference data.

## Tool Used
scikit-learn's `ColumnTransformer`.

## Design Rationale
The ColumnTransformer selects and orders 57 features correctly. All transformations are set to 'passthrough' because data was already cleaned, scaled, and encoded in Module 1.

| Feature Group | Transformation | Rationale |
| :--- | :--- | :--- |
| **Numeric Features** | `passthrough` | Data is already scaled [0, 1]. |
| **Categorical Features (OHE)** | `passthrough` | Data is already encoded [0, 1]. |
| **Excluded Columns** | `drop` | IDs and Targets are excluded from model input. |

## Final Output Structure
The pipeline transforms the DataFrame of features (X) into a NumPy array of size (N, 57), ready for direct model input.
