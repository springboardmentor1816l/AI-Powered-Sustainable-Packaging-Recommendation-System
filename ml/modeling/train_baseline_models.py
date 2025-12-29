"""
EcoPackAI - Baseline Model Training & Evaluation
Trains baseline models and computes evaluation metrics for cost and CO₂ prediction

Author: EcoPackAI Team
Date: 2025-12-26
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_validate, StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import json
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration
RANDOM_SEED = 42
N_FOLDS = 5

# Define directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
ML_DIR = BASE_DIR / 'ml'
METRICS_DIR = ML_DIR / 'metrics'
MODELS_DIR = ML_DIR / 'models'
DOCS_DIR = BASE_DIR / 'docs'
PROCESSED_DIR = DATA_DIR / 'processed'

# Create directories
METRICS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print(" " * 20 + "ECOPACKAI - BASELINE MODEL TRAINING")
print("="*80)


# ==============================================================================
# STEP 1: LOAD DATA
# ==============================================================================

def load_data():
    """Load integrated dataset and prepare for modeling"""
    print("\n" + "="*80)
    print("STEP 1: LOADING DATA")
    print("="*80)
    
    # Load integrated dataset
    data_path = PROCESSED_DIR / 'cleaned_integrated_materials.csv'
    print(f"\n📥 Loading data from: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"✓ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Define features (X) and targets (Y)
    print(f"\n🎯 Defining features and targets...")
    
    # Exclude ID columns and target variables
    exclude_cols = ['material_id', 'suitable_product_categories', 
                   'recommended_packaging_use_cases', 'cost_per_unit_usd', 
                   'co2_emission_per_kg_estimated']
    
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    target_cols = ['cost_per_unit_usd', 'co2_emission_per_kg_estimated']
    
    # Prepare X (features)
    X = df[feature_cols].copy()
    
    # Handle categorical columns - encode them
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    
    print(f"\n📊 Dataset Information:")
    print(f"  - Total samples: {len(df)}")
    print(f"  - Feature columns: {len(feature_cols)}")
    print(f"  - Categorical features: {len(categorical_cols)}")
    print(f"  - Numeric features: {len(feature_cols) - len(categorical_cols)}")
    print(f"  - Target variables: {len(target_cols)}")
    
    # Encode categorical variables
    print(f"\n🔧 Encoding categorical variables...")
    label_encoders = {}
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
        print(f"  ✓ Encoded {col}: {len(le.classes_)} categories")
    
    # Prepare Y (targets)
    Y = df[target_cols].copy()
    
    print(f"\n✅ Data preparation complete")
    print(f"  - X shape: {X.shape}")
    print(f"  - Y shape: {Y.shape}")
    
    return X, Y, df, label_encoders


# ==============================================================================
# STEP 2: CREATE TRAIN/TEST SPLIT
# ==============================================================================

def create_train_test_split(X, Y, df):
    """Create stratified train/test split"""
    print("\n" + "="*80)
    print("STEP 2: CREATING TRAIN/TEST SPLIT")
    print("="*80)
    
    print(f"\n📊 Split Configuration:")
    print(f"  - Strategy: Stratified by material_type")
    print(f"  - Train/Test Ratio: 80% / 20%")
    print(f"  - Random Seed: {RANDOM_SEED}")
    
    # Use material_type for stratification
    stratify_labels = LabelEncoder().fit_transform(df['material_type'])
    
    # Split the data
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y,
        train_size=0.8,
        random_state=RANDOM_SEED,
        stratify=stratify_labels,
        shuffle=True
    )
    
    print(f"\n✅ Split created:")
    print(f"  - Training samples: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  - Testing samples: {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")
    
    return X_train, X_test, Y_train, Y_test


# ==============================================================================
# STEP 3: DEFINE BASELINE MODELS
# ==============================================================================

def define_baseline_models():
    """Define baseline models for each target"""
    print("\n" + "="*80)
    print("STEP 3: DEFINING BASELINE MODELS")
    print("="*80)
    
    models = {
        'cost_per_unit_usd': {
            'name': 'Linear Regression',
            'model': LinearRegression(),
            'rationale': 'Simple linear model to establish baseline cost prediction',
            'assumptions': 'Linear relationship between features and cost'
        },
        'co2_emission_per_kg_estimated': {
            'name': 'Decision Tree Regressor',
            'model': DecisionTreeRegressor(random_state=RANDOM_SEED, max_depth=5),
            'rationale': 'Tree-based model captures non-linear patterns in CO2 emissions',
            'assumptions': 'Piecewise constant approximation with depth limit'
        }
    }
    
    print(f"\n📋 Baseline Models Defined:")
    for target, config in models.items():
        print(f"\n  Target: {target}")
        print(f"    Model: {config['name']}")
        print(f"    Rationale: {config['rationale']}")
        print(f"    Assumptions: {config['assumptions']}")
    
    return models


# ==============================================================================
# STEP 4: TRAIN AND EVALUATE MODELS
# ==============================================================================

def train_and_evaluate_model(model, X_train, y_train, X_test, y_test, model_name, target_name):
    """Train a model and compute evaluation metrics"""
    print(f"\n{'='*80}")
    print(f"Training {model_name} for {target_name}")
    print(f"{'='*80}")
    
    # Train the model
    print(f"\n🔧 Training model...")
    model.fit(X_train, y_train)
    print(f"✓ Model trained successfully")
    
    # Make predictions
    print(f"\n📊 Making predictions...")
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    
    # Compute metrics
    print(f"\n📈 Computing metrics...")
    
    # Training metrics
    train_mae = mean_absolute_error(y_train, train_preds)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_preds))
    train_r2 = r2_score(y_train, train_preds)
    
    # Testing metrics
    test_mae = mean_absolute_error(y_test, test_preds)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_preds))
    test_r2 = r2_score(y_test, test_preds)
    
    # Display results
    print(f"\n  Training Set Performance:")
    print(f"    MAE:  {train_mae:.4f}")
    print(f"    RMSE: {train_rmse:.4f}")
    print(f"    R²:   {train_r2:.4f}")
    
    print(f"\n  Test Set Performance:")
    print(f"    MAE:  {test_mae:.4f}")
    print(f"    RMSE: {test_rmse:.4f}")
    print(f"    R²:   {test_r2:.4f}")
    
    # Check for overfitting
    overfit_check = train_r2 - test_r2
    if overfit_check > 0.1:
        print(f"\n  ⚠️  Warning: Possible overfitting detected (R² difference: {overfit_check:.4f})")
    else:
        print(f"\n  ✓ Good generalization (R² difference: {overfit_check:.4f})")
    
    metrics = {
        'model_name': model_name,
        'target': target_name,
        'train_mae': train_mae,
        'train_rmse': train_rmse,
        'train_r2': train_r2,
        'test_mae': test_mae,
        'test_rmse': test_rmse,
        'test_r2': test_r2,
        'overfit_indicator': overfit_check
    }
    
    return model, metrics, train_preds, test_preds


def perform_cross_validation(model, X_train, y_train, model_name, target_name):
    """Perform cross-validation and return metrics"""
    print(f"\n🔄 Performing {N_FOLDS}-fold cross-validation...")
    
    # Define scoring metrics
    scoring = {
        'neg_mae': 'neg_mean_absolute_error',
        'neg_rmse': 'neg_root_mean_squared_error',
        'r2': 'r2'
    }
    
    # Perform cross-validation
    cv_results = cross_validate(
        model, X_train, y_train,
        cv=N_FOLDS,
        scoring=scoring,
        return_train_score=True,
        n_jobs=-1
    )
    
    # Extract and convert metrics (neg_ metrics need to be negated)
    cv_metrics = {
        'cv_train_mae_mean': -cv_results['train_neg_mae'].mean(),
        'cv_train_mae_std': cv_results['train_neg_mae'].std(),
        'cv_test_mae_mean': -cv_results['test_neg_mae'].mean(),
        'cv_test_mae_std': cv_results['test_neg_mae'].std(),
        'cv_train_rmse_mean': -cv_results['train_neg_rmse'].mean(),
        'cv_train_rmse_std': cv_results['train_neg_rmse'].std(),
        'cv_test_rmse_mean': -cv_results['test_neg_rmse'].mean(),
        'cv_test_rmse_std': cv_results['test_neg_rmse'].std(),
        'cv_train_r2_mean': cv_results['train_r2'].mean(),
        'cv_train_r2_std': cv_results['train_r2'].std(),
        'cv_test_r2_mean': cv_results['test_r2'].mean(),
        'cv_test_r2_std': cv_results['test_r2'].std(),
    }
    
    print(f"\n  Cross-Validation Results ({N_FOLDS} folds):")
    print(f"    Test MAE:  {cv_metrics['cv_test_mae_mean']:.4f} ± {cv_metrics['cv_test_mae_std']:.4f}")
    print(f"    Test RMSE: {cv_metrics['cv_test_rmse_mean']:.4f} ± {cv_metrics['cv_test_rmse_std']:.4f}")
    print(f"    Test R²:   {cv_metrics['cv_test_r2_mean']:.4f} ± {cv_metrics['cv_test_r2_std']:.4f}")
    
    return cv_metrics


# ==============================================================================
# STEP 5: SAVE RESULTS
# ==============================================================================

def save_metrics(all_metrics):
    """Save metrics to CSV"""
    print("\n" + "="*80)
    print("SAVING METRICS")
    print("="*80)
    
    # Create DataFrame
    metrics_df = pd.DataFrame(all_metrics)
    
    # Save to CSV
    output_path = METRICS_DIR / 'baseline_metrics.csv'
    metrics_df.to_csv(output_path, index=False)
    
    print(f"\n💾 Metrics saved to: {output_path}")
    print(f"  - Total records: {len(metrics_df)}")
    
    return metrics_df


def save_models(trained_models):
    """Save trained models"""
    print("\n💾 Saving trained models...")
    
    for target, model_info in trained_models.items():
        model_path = MODELS_DIR / f"baseline_{target.replace('_', '-')}.pkl"
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_info['model'], f)
        
        print(f"  ✓ Saved {model_info['name']} to: {model_path}")


def generate_model_summary(models, all_metrics):
    """Generate baseline model summary documentation"""
    print("\n📝 Generating model summary documentation...")
    
    doc_path = DOCS_DIR / 'baseline_model_summary.md'
    
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write("# Baseline Model Summary\n\n")
        f.write("## Overview\n\n")
        f.write(f"This document summarizes the baseline models trained for the EcoPackAI project.\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("---\n\n")
        f.write("## Models Trained\n\n")
        
        for target, config in models.items():
            f.write(f"### {target}\n\n")
            f.write(f"**Model:** {config['name']}\n\n")
            f.write(f"**Rationale:** {config['rationale']}\n\n")
            f.write(f"**Assumptions:** {config['assumptions']}\n\n")
            
            # Find metrics for this target
            target_metrics = [m for m in all_metrics if m['target'] == target][0]
            
            f.write(f"**Performance:**\n")
            f.write(f"- Test MAE: {target_metrics['test_mae']:.4f}\n")
            f.write(f"- Test RMSE: {target_metrics['test_rmse']:.4f}\n")
            f.write(f"- Test R²: {target_metrics['test_r2']:.4f}\n\n")
            
            f.write(f"**Cross-Validation ({N_FOLDS} folds):**\n")
            f.write(f"- CV MAE: {target_metrics['cv_test_mae_mean']:.4f} ± {target_metrics['cv_test_mae_std']:.4f}\n")
            f.write(f"- CV RMSE: {target_metrics['cv_test_rmse_mean']:.4f} ± {target_metrics['cv_test_rmse_std']:.4f}\n")
            f.write(f"- CV R²: {target_metrics['cv_test_r2_mean']:.4f} ± {target_metrics['cv_test_r2_std']:.4f}\n\n")
        
        f.write("---\n\n")
        f.write("## Model Configuration\n\n")
        f.write(f"- **Random Seed:** {RANDOM_SEED}\n")
        f.write(f"- **Train/Test Split:** 80% / 20%\n")
        f.write(f"- **Cross-Validation Folds:** {N_FOLDS}\n")
        f.write(f"- **Stratification:** By material_type\n\n")
        
        f.write("---\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. Compare baseline performance with advanced models\n")
        f.write("2. Investigate feature importance\n")
        f.write("3. Identify areas for improvement\n")
        f.write("4. Tune hyperparameters if needed\n")
    
    print(f"  ✓ Summary saved to: {doc_path}")


def generate_evaluation_report(all_metrics, Y_train, Y_test):
    """Generate detailed evaluation report"""
    print("\n📊 Generating evaluation report...")
    
    doc_path = DOCS_DIR / 'baseline_evaluation_report.md'
    
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write("# Baseline Model Evaluation Report\n\n")
        f.write("## Overview\n\n")
        f.write("This report provides a detailed analysis of baseline model performance ")
        f.write("for the EcoPackAI sustainable packaging recommendation system.\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("---\n\n")
        f.write("## Dataset Statistics\n\n")
        f.write(f"- **Training Samples:** {len(Y_train)}\n")
        f.write(f"- **Test Samples:** {len(Y_test)}\n")
        f.write(f"- **Total Samples:** {len(Y_train) + len(Y_test)}\n\n")
        
        f.write("### Target Variable Statistics\n\n")
        
        for col in Y_train.columns:
            f.write(f"#### {col}\n\n")
            f.write(f"| Statistic | Training | Test |\n")
            f.write(f"|-----------|----------|------|\n")
            f.write(f"| Mean | {Y_train[col].mean():.4f} | {Y_test[col].mean():.4f} |\n")
            f.write(f"| Median | {Y_train[col].median():.4f} | {Y_test[col].median():.4f} |\n")
            f.write(f"| Std Dev | {Y_train[col].std():.4f} | {Y_test[col].std():.4f} |\n")
            f.write(f"| Min | {Y_train[col].min():.4f} | {Y_test[col].min():.4f} |\n")
            f.write(f"| Max | {Y_train[col].max():.4f} | {Y_test[col].max():.4f} |\n\n")
        
        f.write("---\n\n")
        f.write("## Model Performance Comparison\n\n")
        
        # Create comparison table
        f.write("| Target | Model | Test MAE | Test RMSE | Test R² | CV R² |\n")
        f.write("|--------|-------|----------|-----------|---------|-------|\n")
        
        for metrics in all_metrics:
            f.write(f"| {metrics['target']} | {metrics['model_name']} | ")
            f.write(f"{metrics['test_mae']:.4f} | {metrics['test_rmse']:.4f} | ")
            f.write(f"{metrics['test_r2']:.4f} | {metrics['cv_test_r2_mean']:.4f} |\n")
        
        f.write("\n---\n\n")
        f.write("## Key Findings\n\n")
        
        # Analyze each target
        for metrics in all_metrics:
            f.write(f"### {metrics['target']}\n\n")
            f.write(f"**Model:** {metrics['model_name']}\n\n")
            
            # Interpret R² score
            r2 = metrics['test_r2']
            if r2 >= 0.7:
                r2_interpretation = "Good"
            elif r2 >= 0.5:
                r2_interpretation = "Moderate"
            elif r2 >= 0.3:
                r2_interpretation = "Fair"
            else:
                r2_interpretation = "Poor"
            
            f.write(f"**Performance Assessment:** {r2_interpretation}\n\n")
            f.write(f"- The model explains {r2*100:.1f}% of the variance in {metrics['target']}\n")
            
            # Check overfitting
            if metrics['overfit_indicator'] > 0.1:
                f.write(f"- ⚠️ Shows signs of overfitting (train-test R² gap: {metrics['overfit_indicator']:.4f})\n")
            else:
                f.write(f"- ✓ Good generalization to test data\n")
            
            # Cross-validation consistency
            cv_std = metrics['cv_test_r2_std']
            if cv_std < 0.05:
                f.write(f"- ✓ Consistent performance across folds (σ = {cv_std:.4f})\n")
            else:
                f.write(f"- ⚠️ Variable performance across folds (σ = {cv_std:.4f})\n")
            
            f.write("\n")
        
        f.write("---\n\n")
        f.write("## Recommendations\n\n")
        f.write("1. **Feature Engineering:** Investigate engineered features to improve predictions\n")
        f.write("2. **Advanced Models:** Test ensemble methods (Random Forest, Gradient Boosting)\n")
        f.write("3. **Hyperparameter Tuning:** Optimize model parameters for better performance\n")
        f.write("4. **Feature Selection:** Identify and retain most important features\n")
        f.write("5. **Error Analysis:** Examine residuals to understand model limitations\n\n")
        
        f.write("---\n\n")
        f.write("## Conclusion\n\n")
        f.write("These baseline models provide a starting point for cost and CO₂ prediction. ")
        f.write("The metrics established here will serve as benchmarks for evaluating ")
        f.write("more sophisticated models and optimization strategies.\n")
    
    print(f"  ✓ Evaluation report saved to: {doc_path}")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main execution function"""
    
    # Step 1: Load data
    X, Y, df, label_encoders = load_data()
    
    # Step 2: Create train/test split
    X_train, X_test, Y_train, Y_test = create_train_test_split(X, Y, df)
    
    # Step 3: Define baseline models
    models = define_baseline_models()
    
    # Step 4: Train and evaluate models
    print("\n" + "="*80)
    print("STEP 4: TRAINING AND EVALUATING MODELS")
    print("="*80)
    
    all_metrics = []
    trained_models = {}
    
    for target_col in Y_train.columns:
        print(f"\n{'='*80}")
        print(f"Processing Target: {target_col}")
        print(f"{'='*80}")
        
        # Get model configuration
        model_config = models[target_col]
        model = model_config['model']
        model_name = model_config['name']
        
        # Extract target values
        y_train = Y_train[target_col]
        y_test = Y_test[target_col]
        
        # Train and evaluate
        trained_model, metrics, train_preds, test_preds = train_and_evaluate_model(
            model, X_train, y_train, X_test, y_test, model_name, target_col
        )
        
        # Perform cross-validation
        cv_metrics = perform_cross_validation(
            model, X_train, y_train, model_name, target_col
        )
        
        # Combine metrics
        combined_metrics = {**metrics, **cv_metrics}
        all_metrics.append(combined_metrics)
        
        # Store trained model
        trained_models[target_col] = {
            'model': trained_model,
            'name': model_name,
            'config': model_config
        }
    
    # Step 5: Save results
    print("\n" + "="*80)
    print("STEP 5: SAVING RESULTS")
    print("="*80)
    
    # Save metrics
    metrics_df = save_metrics(all_metrics)
    
    # Save models
    save_models(trained_models)
    
    # Generate documentation
    generate_model_summary(models, all_metrics)
    generate_evaluation_report(all_metrics, Y_train, Y_test)
    
    # Final summary
    print("\n" + "="*80)
    print("BASELINE MODEL TRAINING COMPLETE!")
    print("="*80)
    
    print(f"\n📦 Deliverables:")
    print(f"  1. Metrics CSV: {METRICS_DIR / 'baseline_metrics.csv'}")
    print(f"  2. Model Summary: {DOCS_DIR / 'baseline_model_summary.md'}")
    print(f"  3. Evaluation Report: {DOCS_DIR / 'baseline_evaluation_report.md'}")
    
    print(f"\n✅ Validation Checklist:")
    print(f"  ✓ Baseline models trained successfully")
    print(f"  ✓ Metrics computed for all targets")
    print(f"  ✓ Cross-validation results recorded")
    print(f"  ✓ Metrics stored in CSV format")
    print(f"  ✓ Evaluation report completed")
    
    print(f"\n📊 Performance Summary:")
    for metrics in all_metrics:
        print(f"\n  {metrics['target']}:")
        print(f"    Model: {metrics['model_name']}")
        print(f"    Test R²: {metrics['test_r2']:.4f}")
        print(f"    Test MAE: {metrics['test_mae']:.4f}")
        print(f"    CV R²: {metrics['cv_test_r2_mean']:.4f} ± {metrics['cv_test_r2_std']:.4f}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
