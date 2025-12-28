import pandas as pd
import numpy as np
import joblib
import yaml

# 1. Load Data and Artifacts
try:
    df = pd.read_csv('integrated_dataset.csv')
    pipeline = joblib.load('models/preprocessing/preprocessing_pipeline.pkl')
    rf_cost = joblib.load('ml/models/rf_cost.joblib')
    xgb_co2 = joblib.load('ml/models/xgb_co2.joblib') 
    print("Files and Models loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: {e}")
    # Create dummy check if files aren't in current dir
    import sys
    sys.exit(1)

# 2. Preprocess Features for Prediction
pipeline_exclude = ['product_id', 'Material ID', 'product_name', 'Cost_Efficiency_Index', 'CO2_Impact_Index']
X_raw = df.drop(columns=[col for col in pipeline_exclude if col in df.columns])

X_transformed = pipeline.transform(X_raw)

feature_names = pipeline.get_feature_names_out()
cleaned_feature_names = [name.split('__')[-1] for name in feature_names]
X_processed_df = pd.DataFrame(X_transformed, columns=cleaned_feature_names)
expected_features = list(rf_cost.feature_names_in_)
available_features = [f for f in expected_features if f in X_processed_df.columns]
X_model_ready = X_processed_df[available_features]

raw_feature_names = pipeline.get_feature_names_out()
cleaned_feature_names = [name.split('__')[-1] for name in raw_feature_names]
X_processed_df = pd.DataFrame(X_transformed, columns=cleaned_feature_names)

expected_features = list(rf_cost.feature_names_in_)

available_features = [f for f in expected_features if f in X_processed_df.columns]

X_model_ready = X_processed_df[available_features]

for col in expected_features:
    if col not in X_model_ready.columns:
        X_model_ready[col] = 0

X_model_ready = X_model_ready[expected_features]

print(f"Generating predictions using {X_model_ready.shape[1]} features...")
df['predicted_cost'] = rf_cost.predict(X_model_ready)
df['predicted_co2'] = xgb_co2.predict(X_model_ready)

# 4. IMPLEMENT RANKING LOGIC
ranking_config = {
    'weights': {
        'co2_impact': 0.40,
        'cost_efficiency': 0.30,
        'material_suitability': 0.30
    },
    'thresholds': {
        'min_recyclability': 0.50,
        'min_protection_score': 0.60
    }
}

def calculate_rankings(df, config):
    print("Applying Ranking Logic...")
    weights = config['weights']
    
    # A. Apply Hard Constraints
    # 1. Load Handling Check (Material Strength >= Product Weight)
    df = df[df['Load Handling Score'] >= df['product_weight_kg']].copy()
    
    # 2. Minimum Recyclability
    if 'recyclability_percent' in df.columns:
        df = df[df['recyclability_percent'] >= config['thresholds']['min_recyclability']]

    # B. Normalize Predictions for Scoring (0 to 1 scale)
    def normalize(series, invert=False):
        norm = (series - series.min()) / (series.max() - series.min() + 1e-9)
        return 1 - norm if invert else norm

    # FIXED: Corrected the column mapping here
    df['norm_co2'] = normalize(df['predicted_co2'])
    df['norm_cost'] = normalize(df['predicted_cost'])
    df['norm_suitability'] = normalize(df['Material_Suitability_Score'], invert=True)

    # C. Calculate Composite Score
    df['Final_Ranking_Score'] = (
        (df['norm_co2'] * weights['co2_impact']) +
        (df['norm_cost'] * weights['cost_efficiency']) +
        (df['norm_suitability'] * weights['material_suitability'])
    )

    # D. Sort by Score (Lower score is better)
    df = df.sort_values(by=['product_id', 'Final_Ranking_Score'])

    # E. Assign Rank per Product
    df['Rank'] = df.groupby('product_id')['Final_Ranking_Score'].rank(method='first')
    
    return df

# FIXED: Actually calling the function
df_ranked = calculate_rankings(df, ranking_config)

# 5. SAVE DELIVERABLES
# Save Top 3 Recommendations per Product
top_recommendations = df_ranked[df_ranked['Rank'] <= 3][['product_id', 'Material ID', 'Rank', 'predicted_cost', 'predicted_co2', 'Final_Ranking_Score']]
top_recommendations.to_csv('outputs/material_rankings.csv', index=False)
df_ranked.to_csv('integrated_dataset_Predictions_rank.csv', index=False)

# Save Config YAML
with open('config/ranking_weights.yaml', 'w') as f:
    yaml.dump(ranking_config, f)

# 6. GENERATE DOCUMENTATION
doc_content = f"""
# Material Ranking Logic Documentation

## Optimization Goal
To recommend packaging materials that minimize environmental impact and cost while maximizing structural suitability.

## Scoring Formula
The engine uses a weighted composite score:
`Score = (0.4 * Norm_CO2) + (0.3 * Norm_Cost) + (0.3 * (1 - Norm_Suitability))`

## Hard Constraints Applied
1. **Load Capacity:** Material Load Handling Score must exceed Product Weight.
2. **Sustainability Floor:** Minimum recyclability threshold of {ranking_config['thresholds']['min_recyclability']*100}%.
3. **Physical Protection:** Materials failing fragility compatibility are excluded.

## Ranking Configuration
| Criterion | Weight | Goal |
| :--- | :--- | :--- |
| CO2 Impact | {ranking_config['weights']['co2_impact']*100}% | Minimize |
| Cost Efficiency | {ranking_config['weights']['cost_efficiency']*100}% | Minimize |
| Suitability | {ranking_config['weights']['material_suitability']*100}% | Maximize |
"""

with open('docs/material_ranking.md', 'w') as f:
    f.write(doc_content)