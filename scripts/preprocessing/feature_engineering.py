"""
Feature Engineering - EcoPackAI
Create CO₂ Impact Index, Cost Efficiency Index, and Material Suitability Score
"""

import pandas as pd
import numpy as np
from pathlib import Path

def normalize_0_1(series):
    """Normalize series to 0-1 range"""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return series * 0
    return (series - min_val) / (max_val -min_val)

def create_co2_impact_index(df):
    """
    CO₂ Impact Index (0-100, higher is better/greener)
    Formula:
    - Lower CO₂ emissions = better
    - Faster biodegradation = better
    - Higher recyclability = better
    """
    # Normalize CO₂ emission (invert - lower is better)
    co2_norm = 1 - normalize_0_1(df['co2_emission_per_kg_estimated'])
    
    # Biodegradation score (faster degradation = better, use log to handle large values)
    biodeg_score = 1 / np.log1p(df['biodegradation_time_days'])
    biodeg_norm = normalize_0_1(biodeg_score)
    
    # Recyclability bonus (higher is better)
    recyc_norm = df['recyclability_percent'] / 100
    
    # Weighted combination
    cii = (0.4 * co2_norm + 0.3 * biodeg_norm + 0.3 * recyc_norm) * 100
    
    return cii

def create_cost_efficiency_index(df):
    """
    Cost Efficiency Index (0-100, higher is better)
    Formula:
    - Lower cost = better
    - Higher recyclability = cost savings over time
    - Higher reusability = better
    """
    # Cost score (invert - lower cost is better)
    cost_norm = 1 - normalize_0_1(df['cost_per_unit_usd'])
    
    # Recyclability and reusability bonuses
    recyc_bonus = df['recyclability_percent'] / 100
    reuse_bonus = df['reusability_percent'] / 100
    
    # Weighted combination
    cei = (0.5 * cost_norm + 0.3 * recyc_bonus + 0.2 * reuse_bonus) * 100
    
    return cei

def create_material_suitability_score(df):
    """
    Material Suitability Score (0-100)
    Based on physical handling properties
    """
    # Normalize all scores (already on 1-10 scale, convert to 0-1)
    load_norm = (df['load_handling_score'] - 1) / 9
    moisture_norm = (df['moisture_resistance_score'] - 1) / 9
    thermal_norm = (df['thermal_resistance_score'] - 1) / 9
    
    # Average of normalized scores
    mss = ((load_norm + moisture_norm + thermal_norm) / 3) * 100
    
    return mss

def create_overall_sustainability_score(df):
    """
    Overall Sustainability Score
    Weighted average of multiple sustainability factors
    """
    # Normalize components
    recyc_norm = df['recyclability_percent'] / 100
    waste_reduction_norm = df['waste_reduction_impact_percent'] / 100
    cii_norm = df['co2_impact_index'] / 100
    
    # Weighted average
    oss = (0.35 * cii_norm + 0.35 * recyc_norm + 0.3 * waste_reduction_norm) * 100
    
    return oss

def engineer_features(input_path, output_path):
    """Create all engineered features"""
    
    print("="*60)
    print("Feature Engineering")
    print("="*60)
    
    # Load dataset
    df = pd.read_csv(input_path)
    print(f"\n✓ Loaded dataset: {df.shape}")
    
    # Create engineered features
    print("\n1. CO₂ IMPACT INDEX (CII)")
    print("-" * 60)
    df['co2_impact_index'] = create_co2_impact_index(df)
    print(f"✓ Created: Range [{df['co2_impact_index'].min():.2f}, {df['co2_impact_index'].max():.2f}]")
    print(f"  Mean: {df['co2_impact_index'].mean():.2f}, Median: {df['co2_impact_index'].median():.2f}")
    
    print("\n2. COST EFFICIENCY INDEX (CEI)")
    print("-" * 60)
    df['cost_efficiency_index'] = create_cost_efficiency_index(df)
    print(f"✓ Created: Range [{df['cost_efficiency_index'].min():.2f}, {df['cost_efficiency_index'].max():.2f}]")
    print(f"  Mean: {df['cost_efficiency_index'].mean():.2f}, Median: {df['cost_efficiency_index'].median():.2f}")
    
    print("\n3. MATERIAL SUITABILITY SCORE (MSS)")
    print("-" * 60)
    df['material_suitability_score'] = create_material_suitability_score(df)
    print(f"✓ Created: Range [{df['material_suitability_score'].min():.2f}, {df['material_suitability_score'].max():.2f}]")
    print(f"  Mean: {df['material_suitability_score'].mean():.2f}, Median: {df['material_suitability_score'].median():.2f}")
    
    print("\n4. OVERALL SUSTAINABILITY SCORE")
    print("-" * 60)
    df['overall_sustainability_score'] = create_overall_sustainability_score(df)
    print(f"✓ Created: Range [{df['overall_sustainability_score'].min():.2f}, {df['overall_sustainability_score'].max():.2f}]")
    print(f"  Mean: {df['overall_sustainability_score'].mean():.2f}, Median: {df['overall_sustainability_score'].median():.2f}")
    
    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved engineered dataset to: {output_path}")
    print(f"✓ Final shape: {df.shape}")
    
    return df

if __name__ == "__main__":
    input_path = Path("data/processed/cleaned_integrated_materials.csv")
    output_path = Path("data/model_ready/materials_engineered.csv")
    
    df = engineer_features(input_path, output_path)
    print("\n✅ Feature engineering complete!")
