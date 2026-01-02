"""
Material Ranking Demo Script
=============================

This script demonstrates the material ranking system with various configurations
and provides examples of different ranking modes.

Usage:
    python scripts/demo_ranking.py

Author: EcoPackAI Team
Date: 2026-01-02
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from src.recommendation.ranker import MaterialRanker
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_basic_ranking():
    """Demonstrate basic material ranking"""
    print_section("DEMO 1: Basic Material Ranking")
    
    # Initialize ranker
    ranker = MaterialRanker(
        config_path='config/ranking_weights.yaml',
        ranking_mode='balanced'
    )
    
    # Load data
    data_path = 'data/ml_ready/X_raw.csv'
    logger.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)
    
    logger.info(f"Loaded {len(df)} materials")
    logger.info(f"Features: {df.columns.tolist()}")
    
    # Rank materials
    df_ranked = ranker.rank_materials(df)
    
    # Get top 10
    df_top = ranker.get_top_recommendations(df_ranked, top_n=10)
    
    # Display results
    print("\n📊 Top 10 Recommended Materials (Balanced Mode):")
    print("-" * 80)
    
    display_cols = [
        'rank', 'ranking_score', 
        'recyclability_percent', 
        'material_suitability_score',
        'cost_per_unit_usd',
        'co2_emission_per_kg_estimated'
    ]
    
    # Filter columns that exist
    display_cols = [col for col in display_cols if col in df_top.columns]
    
    print(df_top[display_cols].to_string(index=False))
    
    # Export results
    output_path = 'outputs/rankings_balanced.csv'
    ranker.export_rankings(df_top, output_path, format='csv', include_explanations=True)
    logger.info(f"Results exported to {output_path}")
    
    return df_ranked


def demo_ranking_modes():
    """Compare different ranking modes"""
    print_section("DEMO 2: Comparing Ranking Modes")
    
    modes = ['sustainability_first', 'cost_first', 'balanced']
    results = {}
    
    for mode in modes:
        logger.info(f"Running ranking with mode: {mode}")
        
        ranker = MaterialRanker(
            config_path='config/ranking_weights.yaml',
            ranking_mode=mode
        )
        
        df = pd.read_csv('data/ml_ready/X_raw.csv')
        df_ranked = ranker.rank_materials(df)
        df_top = ranker.get_top_recommendations(df_ranked, top_n=5)
        
        results[mode] = df_top
        
        # Export
        output_path = f'outputs/rankings_{mode}.csv'
        ranker.export_rankings(df_top, output_path, format='csv')
        logger.info(f"Exported {mode} results to {output_path}")
    
    # Compare top materials across modes
    print("\n📊 Top Material by Ranking Mode:")
    print("-" * 80)
    print(f"{'Mode':<25} {'Top Material':<30} {'Score':<10}")
    print("-" * 80)
    
    for mode, df_result in results.items():
        if len(df_result) > 0:
            top_row = df_result.iloc[0]
            material_type = top_row.get('material_type', 'N/A')
            score = top_row.get('ranking_score', 0)
            print(f"{mode:<25} {str(material_type)[:28]:<30} {score:.3f}")
    
    print("-" * 80)
    
    return results


def demo_grouped_ranking():
    """Demonstrate grouped ranking by packaging type"""
    print_section("DEMO 3: Grouped Ranking by Packaging Type")
    
    ranker = MaterialRanker(
        config_path='config/ranking_weights.yaml',
        ranking_mode='balanced'
    )
    
    df = pd.read_csv('data/ml_ready/X_raw.csv')
    
    # Check if packaging_type exists
    if 'packaging_type' not in df.columns:
        logger.warning("packaging_type column not found. Skipping grouped ranking demo.")
        return None
    
    # Rank by packaging type
    df_ranked = ranker.rank_materials(df, group_by='packaging_type')
    df_top = ranker.get_top_recommendations(df_ranked, top_n=3, group_by='packaging_type')
    
    # Display results by group
    print("\n📦 Top 3 Materials by Packaging Type:")
    print("-" * 80)
    
    for ptype in sorted(df_top['packaging_type'].unique()):
        print(f"\n{ptype}:")
        subset = df_top[df_top['packaging_type'] == ptype].copy()
        
        display_cols = ['rank', 'ranking_score', 'recyclability_percent']
        display_cols = [col for col in display_cols if col in subset.columns]
        
        for _, row in subset.iterrows():
            print(f"  #{row['rank']}: Score={row['ranking_score']:.3f}, "
                  f"Recyclability={row.get('recyclability_percent', 'N/A')}%")
    
    # Export
    output_path = 'outputs/rankings_by_packaging_type.csv'
    ranker.export_rankings(df_top, output_path, format='csv')
    logger.info(f"Results exported to {output_path}")
    
    return df_top


def demo_constraint_impact():
    """Demonstrate the impact of different constraints"""
    print_section("DEMO 4: Constraint Impact Analysis")
    
    df = pd.read_csv('data/ml_ready/X_raw.csv')
    initial_count = len(df)
    
    print(f"\n📊 Initial dataset: {initial_count} materials")
    print("-" * 80)
    
    # Test with different constraint levels
    constraint_levels = [
        ("Relaxed", {'min_recyclability_percent': 20.0, 'max_cost_per_unit': 150.0}),
        ("Standard", {'min_recyclability_percent': 30.0, 'max_cost_per_unit': 100.0}),
        ("Strict", {'min_recyclability_percent': 50.0, 'max_cost_per_unit': 50.0}),
    ]
    
    results = {}
    
    for level_name, constraints in constraint_levels:
        ranker = MaterialRanker(
            config_path='config/ranking_weights.yaml',
            ranking_mode='balanced'
        )
        
        # Update constraints
        ranker.constraints.update(constraints)
        
        # Apply constraints
        df_filtered = ranker.apply_constraints(df)
        filtered_count = len(df_filtered)
        filtered_pct = (filtered_count / initial_count) * 100
        
        results[level_name] = {
            'count': filtered_count,
            'percentage': filtered_pct
        }
        
        print(f"\n{level_name} Constraints:")
        for key, value in constraints.items():
            print(f"  - {key}: {value}")
        print(f"  ✓ Materials passed: {filtered_count} ({filtered_pct:.1f}%)")
    
    print("\n" + "-" * 80)
    print("\n📊 Constraint Impact Summary:")
    print(f"{'Constraint Level':<20} {'Materials Passed':<20} {'Percentage':<15}")
    print("-" * 80)
    for level_name, data in results.items():
        print(f"{level_name:<20} {data['count']:<20} {data['percentage']:.1f}%")
    print("-" * 80)
    
    return results


def demo_score_breakdown():
    """Show detailed score breakdown for top materials"""
    print_section("DEMO 5: Score Breakdown Analysis")
    
    ranker = MaterialRanker(
        config_path='config/ranking_weights.yaml',
        ranking_mode='balanced'
    )
    
    df = pd.read_csv('data/ml_ready/X_raw.csv')
    df_ranked = ranker.rank_materials(df)
    df_top = ranker.get_top_recommendations(df_ranked, top_n=5)
    
    print("\n📊 Detailed Score Breakdown for Top 5 Materials:")
    print("-" * 80)
    
    score_cols = [col for col in df_top.columns if col.startswith('score_')]
    
    for idx, row in df_top.iterrows():
        rank = row.get('rank', 'N/A')
        total_score = row.get('ranking_score', 0)
        
        print(f"\nRank #{rank} - Total Score: {total_score:.3f}")
        print("  Contributions:")
        
        for score_col in score_cols:
            criterion = score_col.replace('score_', '')
            contribution = row.get(score_col, 0)
            weight = ranker.weights.get(criterion, 0)
            print(f"    • {criterion:25} {contribution:.3f} (weight: {weight*100:.0f}%)")
        
        # Show bonus if applied
        if row.get('sustainability_bonus_applied', False):
            print("    ✓ Sustainability bonus applied!")
    
    print("-" * 80)
    
    return df_top


def generate_summary_report():
    """Generate a comprehensive summary report"""
    print_section("SUMMARY REPORT")
    
    ranker = MaterialRanker(
        config_path='config/ranking_weights.yaml',
        ranking_mode='balanced'
    )
    
    df = pd.read_csv('data/ml_ready/X_raw.csv')
    df_ranked = ranker.rank_materials(df)
    
    print("\n📈 Material Ranking System - Summary Statistics")
    print("-" * 80)
    
    print(f"\n1. Dataset Overview:")
    print(f"   - Total materials evaluated: {len(df)}")
    print(f"   - Materials after filtering: {len(df_ranked)}")
    print(f"   - Filter rate: {(1 - len(df_ranked)/len(df))*100:.1f}%")
    
    print(f"\n2. Ranking Score Statistics:")
    print(f"   - Mean score: {df_ranked['ranking_score'].mean():.3f}")
    print(f"   - Median score: {df_ranked['ranking_score'].median():.3f}")
    print(f"   - Std deviation: {df_ranked['ranking_score'].std():.3f}")
    print(f"   - Min score: {df_ranked['ranking_score'].min():.3f}")
    print(f"   - Max score: {df_ranked['ranking_score'].max():.3f}")
    
    print(f"\n3. Feature Statistics:")
    if 'recyclability_percent' in df_ranked.columns:
        print(f"   - Average recyclability: {df_ranked['recyclability_percent'].mean():.1f}%")
    if 'cost_per_unit_usd' in df_ranked.columns:
        print(f"   - Average cost: ${df_ranked['cost_per_unit_usd'].mean():.2f}")
    if 'co2_emission_per_kg_estimated' in df_ranked.columns:
        print(f"   - Average CO₂: {df_ranked['co2_emission_per_kg_estimated'].mean():.2f} kg")
    if 'material_suitability_score' in df_ranked.columns:
        print(f"   - Average suitability: {df_ranked['material_suitability_score'].mean():.1f}")
    
    print(f"\n4. Configuration:")
    print(f"   - Ranking mode: {ranker.ranking_mode}")
    print(f"   - Normalization: {ranker.normalization_config.get('method', 'min_max')}")
    print(f"   - Active constraints: {len(ranker.constraints)}")
    
    print("\n" + "-" * 80)
    
    # Create summary report file
    report_path = 'outputs/ranking_summary_report.txt'
    with open(report_path, 'w') as f:
        f.write("MATERIAL RANKING SYSTEM - SUMMARY REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {pd.Timestamp.now()}\n\n")
        f.write(f"Total materials: {len(df)}\n")
        f.write(f"Ranked materials: {len(df_ranked)}\n")
        f.write(f"Average score: {df_ranked['ranking_score'].mean():.3f}\n")
        f.write(f"Ranking mode: {ranker.ranking_mode}\n")
    
    logger.info(f"Summary report saved to {report_path}")


def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "MATERIAL RANKING SYSTEM DEMO" + " " * 30 + "║")
    print("║" + " " * 26 + "EcoPackAI Project" + " " * 35 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        # Ensure output directory exists
        Path('outputs').mkdir(exist_ok=True)
        
        # Run demonstrations
        demo_basic_ranking()
        demo_ranking_modes()
        demo_grouped_ranking()
        demo_constraint_impact()
        demo_score_breakdown()
        generate_summary_report()
        
        print_section("ALL DEMOS COMPLETED SUCCESSFULLY! ✓")
        print("\n📁 Output files generated:")
        print("   - outputs/rankings_balanced.csv")
        print("   - outputs/rankings_sustainability_first.csv")
        print("   - outputs/rankings_cost_first.csv")
        print("   - outputs/rankings_by_packaging_type.csv")
        print("   - outputs/ranking_summary_report.txt")
        print("\n✨ Check the outputs directory for detailed results!\n")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error("Please ensure the required data files exist:")
        logger.error("  - data/ml_ready/X_raw.csv")
        logger.error("  - config/ranking_weights.yaml")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)


if __name__ == '__main__':
    main()
