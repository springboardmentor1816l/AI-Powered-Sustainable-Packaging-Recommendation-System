import pandas as pd
from services.model_loader import rf_sustainability_pipeline


def predict_sustainability(payload: dict) -> float:
    # 1️⃣ Convert JSON → DataFrame (1 row)
    df = pd.DataFrame([payload])

    # 2️⃣ Get columns the model was trained on
    expected_cols = rf_sustainability_pipeline.feature_names_in_

    # 3️⃣ Add missing columns with safe default values
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0

    # 4️⃣ Ensure correct column order
    df = df[expected_cols]

    # 5️⃣ Predict
    prediction = rf_sustainability_pipeline.predict(df)

    return float(prediction[0])


