"""
CSV Validation Script for EcoPackAI
Validates CSV files for schema consistency, data quality, and completeness.
"""

import pandas as pd
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json


class CSVValidator:
    """Validates CSV files for quality and schema compliance."""
    
    def __init__(self, csv_path: str):
        """
        Initialize validator with CSV file path.
        
        Args:
            csv_path: Path to CSV file to validate
        """
        self.csv_path = Path(csv_path)
        self.df = None
        self.validation_results = {
            'file_name': self.csv_path.name,
            'file_path': str(self.csv_path),
            'status': 'PENDING',
            'issues': [],
            'warnings': [],
            'info': {}
        }
    
    def load_csv(self) -> bool:
        """Load CSV file and perform basic checks."""
        try:
            self.df = pd.read_csv(self.csv_path)
            self.validation_results['info']['total_rows'] = len(self.df)
            self.validation_results['info']['total_columns'] = len(self.df.columns)
            self.validation_results['info']['columns'] = list(self.df.columns)
            return True
        except FileNotFoundError:
            self.validation_results['issues'].append(f"File not found: {self.csv_path}")
            return False
        except pd.errors.EmptyDataError:
            self.validation_results['issues'].append("CSV file is empty")
            return False
        except Exception as e:
            self.validation_results['issues'].append(f"Error loading CSV: {str(e)}")
            return False
    
    def check_missing_values(self) -> None:
        """Check for missing values in dataset."""
        if self.df is None:
            return
        
        missing_counts = self.df.isnull().sum()
        missing_cols = missing_counts[missing_counts > 0]
        
        if len(missing_cols) > 0:
            for col, count in missing_cols.items():
                percent = (count / len(self.df)) * 100
                if percent > 50:
                    self.validation_results['issues'].append(
                        f"Column '{col}' has {count} ({percent:.2f}%) missing values"
                    )
                elif percent > 10:
                    self.validation_results['warnings'].append(
                        f"Column '{col}' has {count} ({percent:.2f}%) missing values"
                    )
        
        self.validation_results['info']['missing_value_summary'] = missing_counts.to_dict()
    
    def check_duplicates(self) -> None:
        """Check for duplicate rows."""
        if self.df is None:
            return
        
        duplicate_count = self.df.duplicated().sum()
        
        if duplicate_count > 0:
            percent = (duplicate_count / len(self.df)) * 100
            self.validation_results['warnings'].append(
                f"Found {duplicate_count} ({percent:.2f}%) duplicate rows"
            )
            self.validation_results['info']['duplicate_rows'] = int(duplicate_count)
        else:
            self.validation_results['info']['duplicate_rows'] = 0
    
    def check_column_naming(self) -> None:
        """Check if column names follow snake_case convention."""
        if self.df is None:
            return
        
        non_snake_case = []
        for col in self.df.columns:
            # Check for spaces, uppercase, or special characters (except underscore)
            if ' ' in col or col != col.lower() or any(c.isupper() for c in col):
                non_snake_case.append(col)
        
        if non_snake_case:
            self.validation_results['warnings'].append(
                f"Columns not in snake_case: {', '.join(non_snake_case)}"
            )
    
    def check_data_types(self) -> None:
        """Analyze and report data types."""
        if self.df is None:
            return
        
        dtype_info = {}
        for col in self.df.columns:
            dtype_info[col] = str(self.df[col].dtype)
        
        self.validation_results['info']['data_types'] = dtype_info
    
    def check_expected_schema(self, expected_columns: List[str]) -> None:
        """
        Check if CSV has expected columns.
        
        Args:
            expected_columns: List of expected column names
        """
        if self.df is None:
            return
        
        actual_columns = set(self.df.columns)
        expected_set = set(expected_columns)
        
        missing_cols = expected_set - actual_columns
        extra_cols = actual_columns - expected_set
        
        if missing_cols:
            self.validation_results['issues'].append(
                f"Missing expected columns: {', '.join(missing_cols)}"
            )
        
        if extra_cols:
            self.validation_results['warnings'].append(
                f"Unexpected columns found: {', '.join(extra_cols)}"
            )
    
    def validate(self, expected_columns: List[str] = None) -> Dict:
        """
        Run all validation checks.
        
        Args:
            expected_columns: Optional list of expected column names
            
        Returns:
            Dictionary containing validation results
        """
        if not self.load_csv():
            self.validation_results['status'] = 'FAILED'
            return self.validation_results
        
        # Run all checks
        self.check_missing_values()
        self.check_duplicates()
        self.check_column_naming()
        self.check_data_types()
        
        if expected_columns:
            self.check_expected_schema(expected_columns)
        
        # Determine overall status
        if self.validation_results['issues']:
            self.validation_results['status'] = 'FAILED'
        elif self.validation_results['warnings']:
            self.validation_results['status'] = 'PASSED_WITH_WARNINGS'
        else:
            self.validation_results['status'] = 'PASSED'
        
        return self.validation_results
    
    def print_report(self) -> None:
        """Print validation report to console."""
        print(f"\n{'='*70}")
        print(f"CSV Validation Report: {self.validation_results['file_name']}")
        print(f"{'='*70}")
        print(f"Status: {self.validation_results['status']}")
        print(f"\nFile: {self.validation_results['file_path']}")
        
        info = self.validation_results['info']
        print(f"\n📊 Dataset Info:")
        print(f"  - Rows: {info.get('total_rows', 'N/A')}")
        print(f"  - Columns: {info.get('total_columns', 'N/A')}")
        print(f"  - Duplicates: {info.get('duplicate_rows', 'N/A')}")
        
        if self.validation_results['issues']:
            print(f"\n❌ Issues ({len(self.validation_results['issues'])}):")
            for issue in self.validation_results['issues']:
                print(f"  - {issue}")
        
        if self.validation_results['warnings']:
            print(f"\n⚠️  Warnings ({len(self.validation_results['warnings'])}):")
            for warning in self.validation_results['warnings']:
                print(f"  - {warning}")
        
        if not self.validation_results['issues'] and not self.validation_results['warnings']:
            print(f"\n✅ No issues found!")
        
        print(f"\n{'='*70}\n")


def main():
    """Main function to run validation from command line."""
    if len(sys.argv) < 2:
        print("Usage: python validate_csv.py <csv_file_path> [expected_columns_json]")
        print("\nExample:")
        print("  python validate_csv.py data/materials.csv")
        print("  python validate_csv.py data/materials.csv '[\"name\",\"density\",\"cost\"]'")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    expected_columns = None
    
    if len(sys.argv) > 2:
        try:
            expected_columns = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print("Error: Expected columns must be valid JSON array")
            sys.exit(1)
    
    # Run validation
    validator = CSVValidator(csv_path)
    results = validator.validate(expected_columns)
    validator.print_report()
    
    # Exit with appropriate code
    if results['status'] == 'FAILED':
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
