import numpy as np

def preprocess_common(df):
    # Handle missing values
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    return df
