"""
Batch Import Utility for EcoPackAI
Automates ingestion of multiple CSV files based on configuration.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List
import sys

from db_helper import DatabaseHelper
from ingest_data import DataIngestor
from validate_csv import CSVValidator
from clean_data import DataCleaner


class BatchImporter:
    """Batch import utility for multiple datasets."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize batch importer.
        
        Args:
            config_path: Path to configuration file (YAML or JSON)
        """
        self.config_path = config_path
        self.config = None
        self.db = DatabaseHelper()
        self.ingestor = DataIngestor(self.db)
        self.results = {
            'validated': {},
            'cleaned': {},
            'ingested': {}
        }
    
    def load_config(self) -> bool:
        """Load configuration from file."""
        if not self.config_path:
            return False
        
        try:
            config_file = Path(self.config_path)
            
            if config_file.suffix in ['.yaml', '.yml']:
                import yaml
                with open(config_file, 'r') as f:
                    self.config = yaml.safe_load(f)
            elif config_file.suffix == '.json':
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                print(f"Unsupported config file format: {config_file.suffix}")
                return False
            
            print(f"✓ Loaded configuration from {config_file.name}")
            return True
            
        except Exception as e:
            print(f"✗ Error loading config: {e}")
            return False
    
    def validate_datasets(self) -> None:
        """Validate all datasets in configuration."""
        if not self.config or 'datasets' not in self.config:
            return
        
        print(f"\n{'='*70}")
        print("VALIDATION PHASE")
        print(f"{'='*70}\n")
        
        for dataset in self.config['datasets']:
            csv_path = dataset['csv_path']
            expected_columns = dataset.get('expected_columns', None)
            
            print(f"\nValidating: {Path(csv_path).name}")
            print("-" * 70)
            
            validator = CSVValidator(csv_path)
            result = validator.validate(expected_columns)
            validator.print_report()
            
            self.results['validated'][csv_path] = result['status']
    
    def clean_datasets(self) -> None:
        """Clean all datasets in configuration."""
        if not self.config or 'datasets' not in self.config:
            return
        
        print(f"\n{'='*70}")
        print("CLEANING PHASE")
        print(f"{'='*70}\n")
        
        for dataset in self.config['datasets']:
            csv_path = dataset['csv_path']
            output_path = dataset.get('output_path', None)
            missing_strategy = dataset.get('missing_strategy', 'drop')
            type_map = dataset.get('type_map', None)
            
            print(f"\nCleaning: {Path(csv_path).name}")
            print("-" * 70)
            
            try:
                cleaner = DataCleaner(csv_path, output_path)
                cleaner.clean(missing_strategy=missing_strategy, type_map=type_map)
                cleaner.print_log()
                
                self.results['cleaned'][csv_path] = True
                
                # Update csv_path to cleaned version for ingestion
                dataset['csv_path'] = str(cleaner.output_path)
                
            except Exception as e:
                print(f"✗ Cleaning failed: {e}")
                self.results['cleaned'][csv_path] = False
    
    def ingest_datasets(self) -> None:
        """Ingest all datasets into database."""
        if not self.config or 'datasets' not in self.config:
            return
        
        print(f"\n{'='*70}")
        print("INGESTION PHASE")
        print(f"{'='*70}\n")
        
        # Test database connection
        if not self.db.test_connection():
            print("\n✗ Database connection failed! Cannot proceed with ingestion.")
            return
        
        for dataset in self.config['datasets']:
            csv_path = dataset['csv_path']
            table_name = dataset['table_name']
            column_mapping = dataset.get('column_mapping', None)
            
            print(f"\nIngesting into table: {table_name}")
            print("-" * 70)
            
            success = self.ingestor.ingest_csv(csv_path, table_name, column_mapping)
            self.ingestor.print_log()
            
            self.results['ingested'][table_name] = success
            
            # Verify ingestion
            if success:
                self.ingestor.verify_ingestion(table_name)
                self.ingestor.print_log()
    
    def print_summary(self) -> None:
        """Print summary of batch import results."""
        print(f"\n{'='*70}")
        print("BATCH IMPORT SUMMARY")
        print(f"{'='*70}\n")
        
        if self.results['validated']:
            print("Validation Results:")
            for path, status in self.results['validated'].items():
                icon = "✓" if status == "PASSED" else "⚠" if status == "PASSED_WITH_WARNINGS" else "✗"
                print(f"  {icon} {Path(path).name}: {status}")
        
        if self.results['cleaned']:
            print("\nCleaning Results:")
            for path, success in self.results['cleaned'].items():
                icon = "✓" if success else "✗"
                print(f"  {icon} {Path(path).name}")
        
        if self.results['ingested']:
            print("\nIngestion Results:")
            for table, success in self.results['ingested'].items():
                icon = "✓" if success else "✗"
                print(f"  {icon} {table}")
        
        print(f"\n{'='*70}\n")
    
    def run(self, validate: bool = True, clean: bool = True, ingest: bool = True) -> None:
        """
        Run batch import pipeline.
        
        Args:
            validate: Whether to run validation phase
            clean: Whether to run cleaning phase
            ingest: Whether to run ingestion phase
        """
        if not self.load_config():
            print("✗ Failed to load configuration!")
            return
        
        if validate:
            self.validate_datasets()
        
        if clean:
            self.clean_datasets()
        
        if ingest:
            self.ingest_datasets()
        
        self.print_summary()


def create_sample_config(output_path: str = "batch_import_config.yaml") -> None:
    """Create a sample configuration file."""
    sample_config = {
        'datasets': [
            {
                'csv_path': 'data/raw_datasets/materials/materials.csv',
                'table_name': 'materials',
                'output_path': 'data/processed/materials.csv',
                'missing_strategy': 'drop',
                'expected_columns': [
                    'material_id', 'material_type', 'strength_mpa',
                    'weight_capacity', 'biodegradability_percent',
                    'co2_emission_score', 'recyclability_percent',
                    'cost_per_kg', 'industry_use_case'
                ],
                'column_mapping': None
            },
            {
                'csv_path': 'data/raw_datasets/products/products.csv',
                'table_name': 'products',
                'output_path': 'data/processed/products.csv',
                'missing_strategy': 'drop',
                'expected_columns': [
                    'product_id', 'product_name', 'category',
                    'product_weight', 'fragility_index', 'shipping_type'
                ],
                'column_mapping': None
            }
        ]
    }
    
    with open(output_path, 'w') as f:
        yaml.dump(sample_config, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Created sample configuration: {output_path}")


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Batch Import Utility for EcoPackAI")
        print("=" * 70)
        print("\nUsage:")
        print("  python batch_import.py <config_file>")
        print("  python batch_import.py --create-config [output_path]")
        print("\nExamples:")
        print("  python batch_import.py batch_import_config.yaml")
        print("  python batch_import.py --create-config my_config.yaml")
        print("\nConfig file format: YAML or JSON")
        sys.exit(1)
    
    if sys.argv[1] == '--create-config':
        output_path = sys.argv[2] if len(sys.argv) > 2 else 'batch_import_config.yaml'
        create_sample_config(output_path)
        sys.exit(0)
    
    config_path = sys.argv[1]
    
    importer = BatchImporter(config_path)
    importer.run()


if __name__ == "__main__":
    main()
