"""
Simple Material Ranking Test
=============================
Quick test to validate the ranking system with actual data.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.recommendation.ranker import MaterialRanker

# Load data
print("Loading data...")
df = pd.read_csv('data/ml_ready/X_raw.csv')
print(f"Loaded {len(df)} materials")
print(f"Columns: {df.columns.tolist()}")

# Check data statistics
print("\n=== Data Statistics ===")
print(f"\nRecyclability:")
print(f"  Min: {df['recyclability_percent'].min():.1f}%")
print(f"  Max: {df['recyclability_percent'].max():.1f}%")
print(f"  Mean: {df['recyclability_percent'].mean():.1f}%")

if 'cost_per_unit_usd' in df.columns:
    print(f"\nCost:")
    print(f"  Min: ${df['cost_per_unit_usd'].min():.2f}")
    print(f"  Max: ${df['cost_per_unit_usd'].max():.2f}")
    print(f"  Mean: ${df['cost_per_unit_usd'].mean():.2f}")

if 'material_suitability_score' in df.columns:
    print(f"\nMaterial Suitability:")
    print(f"  Min: {df['material_suitability_score'].min():.1f}")
    print(f"  Max: {df['material_suitability_score'].max():.1f}")
    print(f"  Mean: {df['material_suitability_score'].mean():.1f}")

if 'load_handling_score' in df.columns:
    print(f"\nLoad Handling:")
    print(f"  Min: {df['load_handling_score'].min():.1f}")
    print(f"  Max: {df['load_handling_score'].max():.1f}")
    print(f"  Mean: {df['load_handling_score'].mean():.1f}")

# Initialize ranker with relaxed constraints
print("\n=== Initializing Ranker ===")
ranker = MaterialRanker(
    config_path='config/ranking_weights.yaml',
    ranking_mode='balanced'
)

# Relax constraints to ensure we get some results
print("\nRelaxing constraints for testing...")
ranker.constraints = {
    'min_recyclability_percent': 0.0,
    'max_cost_per_unit': 1000.0,
    'min_load_handling_score': 0.0,
    'min_moisture_resistance_score': 0.0,
    'min_thermal_resistance_score': 0.0,
    'min_material_suitability_score': 0.0,
    'min_sustainability_compliance_percent': 0.0
}

# Apply constraints
print("\n=== Applying Constraints ===")
df_filtered = ranker.apply_constraints(df)
print(f"Materials after filtering: {len(df_filtered)}")

if len(df_filtered) == 0:
    print("ERROR: All materials filtered out!")
    sys.exit(1)

# Rank materials
print("\n=== Ranking Materials ===")
df_ranked = ranker.rank_materials(df)
print(f"Ranked {len(df_ranked)} materials")

if len(df_ranked) > 0:
    print(f"\nScore statistics:")
    print(f"  Min: {df_ranked['ranking_score'].min():.3f}")
    print(f"  Max: {df_ranked['ranking_score'].max():.3f}")
    print(f"  Mean: {df_ranked['ranking_score'].mean():.3f}")
    
    # Get top 10
    df_top = ranker.get_top_recommendations(df_ranked, top_n=10)
    
    print("\n=== Top 10 Materials ===")
    print(df_top[['rank', 'ranking_score', 
                  'recyclability_percent', 
                  'cost_per_unit_usd',
                  'material_suitability_score']].to_string(index=False))
    
    # Export
    print("\n=== Exporting Results ===")
    ranker.export_rankings(df_top, 'outputs/test_rankings.csv', format='csv', include_explanations=True)
    print("✓ Exported to outputs/test_rankings.csv")
    
    # Also export JSON
    ranker.export_rankings(df_top, 'outputs/test_rankings.json', format='json', include_explanations=True)
    print("✓ Exported to outputs/test_rankings.json")
    
    print("\n=== Test Completed Successfully! ===")
else:
    print("ERROR: No materials ranked!")
