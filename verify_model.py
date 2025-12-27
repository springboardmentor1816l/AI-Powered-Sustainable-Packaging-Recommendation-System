
import pandas as pd
import joblib
import os

def verify():
    model_path = "ml/models/training/packaging_model_v1.0.pkl"
    X_path = "notebooks/data/final/X_raw.csv"
    y_path = "notebooks/data/final/y_raw.csv"

    if not os.path.exists(model_path):
        print("? Model file not found! Please check the path.")
        return

    # Load everything
    model = joblib.load(model_path)
    X = pd.read_csv(X_path)
    y = pd.read_csv(y_path)

    # Pick 3 different rows to see variety
    for i in [0, 5, 10]:
        sample_input = X.iloc[[i]]
        actual_material = y.iloc[i, 0]
        
        # AI makes a guess
        prediction = model.predict(sample_input)[0]

        print(f"\n--- Product Test {i+1} ---")
        print(f"Features: Weight={sample_input.iloc[0,0]}, Fragility={sample_input.iloc[0,1]}")
        print(f"AI Guess: {prediction}")
        print(f"Real Label: {actual_material}")
        
        if str(prediction) == str(actual_material):
            print("? Status: Correct Prediction")
        else:
            print("?? Status: Incorrect Prediction")

if __name__ == "__main__":
    verify()

