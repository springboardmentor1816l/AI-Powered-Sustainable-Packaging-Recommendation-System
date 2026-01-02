"""
Material Ranking Production Script
===================================

This script generates material rankings for production use.
It supports multiple ranking modes and can integrate model predictions.

Usage:
    # Basic usage with default settings
    python scripts/generate_rankings.py
    
    # With specific ranking mode
    python scripts/generate_rankings.py --mode sustainability_first
    
    # With model predictions
    python scripts/generate_rankings.py --predictions outputs/predictions.csv
    
    # Group by packaging type
    python scripts/generate_rankings.py --group-by packaging_type --top-n 5

Author: EcoPackAI Team
Date: 2026-01-02
"""

import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import logging
from src.recommendation.ranker import MaterialRanker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Generate material rankings for sustainable packaging'
    )
    
    parser.add_argument(
        '--data',
        type=str,
        default='data/ml_ready/X_raw.csv',
        help='Path to feature dataset'
    )
    
    parser.add_argument(
        '--predictions',
        type=str,
        default=None,
        help='Optional path to model predictions CSV'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/ranking_weights.yaml',
        help='Path to ranking configuration file'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        default='balanced',
        choices=['sustainability_first', 'cost_first', 'balanced'],
        help='Ranking mode to use'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='outputs/material_rankings.csv',
        help='Path to save ranked materials'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        default='csv',
        choices=['csv', 'json', 'excel'],
        help='Output file format'
    )
    
    parser.add_argument(
        '--group-by',
        type=str,
        default=None,
        help='Optional column to group rankings by (e.g., packaging_type)'
    )
    
    parser.add_argument(
        '--top-n',
        type=int,
        default=10,
        help='Number of top materials to recommend'
    )
    
    parser.add_argument(
        '--no-explanations',
        action='store_true',
        help='Exclude explanations from output'
    )
    
    parser.add_argument(
        '--generate-all-modes',
        action='store_true',
        help='Generate rankings for all three modes'
    )
    
    return parser.parse_args()


def generate_rankings_for_mode(
    ranker: MaterialRanker,
    df: pd.DataFrame,
    predictions_df: pd.DataFrame,
    mode: str,
    group_by: str,
    top_n: int,
    output_path: str,
    output_format: str,
    include_explanations: bool
) -> pd.DataFrame:
    """
    Generate rankings for a specific mode
    
    Args:
        ranker: MaterialRanker instance
        df: Feature DataFrame
        predictions_df: Predictions DataFrame (optional)
        mode: Ranking mode
        group_by: Column to group by
        top_n: Number of top materials
        output_path: Output file path
        output_format: Output format
        include_explanations: Include explanations
        
    Returns:
        DataFrame with ranked materials
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"Generating rankings with mode: {mode}")
    logger.info(f"{'='*60}")
    
    # Update mode
    ranker.ranking_mode = mode
    if mode in ranker.config_weights:
        ranker.weights = ranker.config_weights[mode]
        ranker._validate_config()
    
    # Prepare data
    df_input = df.copy()
    
    # Merge predictions if available
    if predictions_df is not None:
        logger.info("Merging model predictions...")
        if 'predicted_cost' in predictions_df.columns:
            df_input['predicted_cost'] = predictions_df['predicted_cost']
            logger.info("✓ Added predicted cost")
        if 'predicted_co2' in predictions_df.columns:
            df_input['predicted_co2'] = predictions_df['predicted_co2']
            logger.info("✓ Added predicted CO₂")
    
    # Rank materials
    logger.info("\nRanking materials...")
    df_ranked = ranker.rank_materials(df_input, group_by=group_by)
    
    if len(df_ranked) == 0:
        logger.error("No materials passed constraint filtering!")
        logger.error("Consider relaxing constraints in the configuration file.")
        return pd.DataFrame()
    
    # Get top recommendations
    df_top = ranker.get_top_recommendations(df_ranked, top_n=top_n, group_by=group_by)
    
    # Export
    logger.info(f"\nExporting results to {output_path}")
    ranker.export_rankings(
        df_top, 
        output_path, 
        format=output_format,
        include_explanations=include_explanations
    )
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("RANKING SUMMARY")
    logger.info("="*60)
    logger.info(f"Ranking mode: {mode}")
    logger.info(f"Total materials: {len(df)}")
    logger.info(f"Passed constraints: {len(df_ranked)}")
    logger.info(f"Top recommendations: {len(df_top)}")
    logger.info(f"Average score: {df_ranked['ranking_score'].mean():.3f}")
    logger.info(f"Score range: [{df_ranked['ranking_score'].min():.3f}, {df_ranked['ranking_score'].max():.3f}]")
    
    if group_by and group_by in df_top.columns:
        n_groups = df_top[group_by].nunique()
        logger.info(f"Groups: {n_groups}")
    
    logger.info("="*60 + "\n")
    
    return df_top


def main():
    """Main execution function"""
    args = parse_args()
    
    print("\n╔" + "═"*78 + "╗")
    print("║" + " "*22 + "MATERIAL RANKING GENERATOR" + " "*30 + "║")
    print("║" + " "*27 + "EcoPackAI Project" + " "*34 + "║")
    print("╚" + "═"*78 + "╝\n")
    
    try:
        # Ensure output directory exists
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load feature dataset
        logger.info(f"Loading feature dataset from {args.data}")
        if not Path(args.data).exists():
            logger.error(f"Feature dataset not found: {args.data}")
            return 1
        
        df = pd.read_csv(args.data)
        logger.info(f"✓ Loaded {len(df)} materials with {len(df.columns)} features")
        
        # Load predictions if provided
        predictions_df = None
        if args.predictions:
            if Path(args.predictions).exists():
                logger.info(f"Loading predictions from {args.predictions}")
                predictions_df = pd.read_csv(args.predictions)
                logger.info(f"✓ Loaded {len(predictions_df)} predictions")
            else:
                logger.warning(f"Predictions file not found: {args.predictions}")
        
        # Initialize ranker
        logger.info(f"Initializing MaterialRanker with config: {args.config}")
        ranker = MaterialRanker(
            config_path=args.config,
            ranking_mode=args.mode
        )
        logger.info("✓ Ranker initialized")
        
        include_explanations = not args.no_explanations
        
        if args.generate_all_modes:
            # Generate rankings for all modes
            logger.info("\n🔄 Generating rankings for all modes...")
            
            modes = ['sustainability_first', 'cost_first', 'balanced']
            all_results = {}
            
            for mode in modes:
                mode_output = output_path.parent / f"{output_path.stem}_{mode}{output_path.suffix}"
                
                df_result = generate_rankings_for_mode(
                    ranker=ranker,
                    df=df,
                    predictions_df=predictions_df,
                    mode=mode,
                    group_by=args.group_by,
                    top_n=args.top_n,
                    output_path=str(mode_output),
                    output_format=args.format,
                    include_explanations=include_explanations
                )
                
                all_results[mode] = df_result
            
            # Create comparison summary
            logger.info("\n📊 Mode Comparison Summary:")
            logger.info("-" * 80)
            logger.info(f"{'Mode':<25} {'Top Material Rank':<20} {'Score':<10}")
            logger.info("-" * 80)
            
            for mode, df_result in all_results.items():
                if len(df_result) > 0:
                    top_score = df_result.iloc[0]['ranking_score']
                    logger.info(f"{mode:<25} #{1:<19} {top_score:.3f}")
                else:
                    logger.info(f"{mode:<25} {'No results':<20} {'N/A':<10}")
            
            logger.info("-" * 80)
            
            logger.info("\n✨ Generated rankings for all modes successfully!")
            logger.info(f"\n📁 Output files:")
            for mode in modes:
                mode_output = output_path.parent / f"{output_path.stem}_{mode}{output_path.suffix}"
                logger.info(f"   - {mode_output}")
        
        else:
            # Generate rankings for single mode
            df_result = generate_rankings_for_mode(
                ranker=ranker,
                df=df,
                predictions_df=predictions_df,
                mode=args.mode,
                group_by=args.group_by,
                top_n=args.top_n,
                output_path=args.output,
                output_format=args.format,
                include_explanations=include_explanations
            )
            
            if len(df_result) > 0:
                # Display top 5 results
                logger.info("\n📊 Top 5 Recommended Materials:")
                logger.info("-" * 80)
                
                display_cols = [
                    'rank', 'ranking_score', 
                    'recyclability_percent', 
                    'material_suitability_score'
                ]
                
                # Add cost and CO2 if available
                if 'predicted_cost' in df_result.columns:
                    display_cols.append('predicted_cost')
                elif 'cost_per_unit_usd' in df_result.columns:
                    display_cols.append('cost_per_unit_usd')
                
                if 'predicted_co2' in df_result.columns:
                    display_cols.append('predicted_co2')
                elif 'co2_emission_per_kg_estimated' in df_result.columns:
                    display_cols.append('co2_emission_per_kg_estimated')
                
                display_cols = [col for col in display_cols if col in df_result.columns]
                
                print(df_result.head()[display_cols].to_string(index=False))
                logger.info("-" * 80)
                
                logger.info(f"\n✨ Rankings generated successfully!")
                logger.info(f"📁 Output: {args.output}")
        
        print("\n✅ Material Ranking Complete!\n")
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
