## Preprocessing Pipeline Design

A ColumnTransformer-based preprocessing pipeline was implemented to ensure
consistent data transformation across training and inference.

Numeric features are median-imputed and standardized.
Categorical features are mode-imputed and one-hot encoded.
Binary features are converted to numeric form.

Excluded columns such as IDs and target variables are not passed through
the pipeline to prevent data leakage.

The pipeline is serialized for reuse in downstream modeling stages.
