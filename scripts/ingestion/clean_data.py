"""
Data Cleaning Script for EcoPackAI
Cleans and standardizes CSV files for database ingestion.
"""

import pandas as pd
import sys
from pathlib import Path
import re


class DataCleaner:
    """Cleans and standardizes CSV data."""
    
    def __init__(self, input_path: str, output_path: str = None):
        """
        Initialize data cleaner.
        
        Args:
            input_path: Path to input CSV file
            output_path: Optional output path (defaults to processed/ directory)
        """
        self.input_path = Path(input_path)
        self.output_path = output_path
        
        if not self.output_path:
            # Default to processed directory
            processed_dir = self.input_path.parent.parent / 'processed'
            processed_dir.mkdir(parents=True, exist_ok=True)
            self.output_path = processed_dir / f"cleaned_{self.input_path.name}"
        else:
            self.output_path = Path(output_path)
        
        self.df = None
        self.cleaning_log = []
    
    def load_data(self) -> bool:
        """Load CSV file."""
        try:
            self.df = pd.read_csv(self.input_path)
            self.cleaning_log.append(f"✓ Loaded {len(self.df)} rows from {self.input_path.name}")
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def standardize_column_names(self) -> None:
        """Convert column names to snake_case."""
        original_columns = self.df.columns.tolist()
        
        new_columns = []
        for col in original_columns:
            # Convert to lowercase
            new_col = col.lower()
            # Replace spaces and special chars with underscores
            new_col = re.sub(r'[^a-z0-9]+', '_', new_col)
            # Remove leading/trailing underscores
            new_col = new_col.strip('_')
            # Remove multiple consecutive underscores
            new_col = re.sub(r'_+', '_', new_col)
            new_columns.append(new_col)
        
        self.df.columns = new_columns
        
        changed = [f"{old} → {new}" for old, new in zip(original_columns, new_columns) 
                   if old != new]
        if changed:
            self.cleaning_log.append(f"✓ Standardized {len(changed)} column names")
    
    def remove_duplicates(self) -> None:
        """Remove duplicate rows."""
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_count - len(self.df)
        
        if removed > 0:
            self.cleaning_log.append(f"✓ Removed {removed} duplicate rows")
    
    def handle_missing_values(self, strategy: str = 'drop') -> None:
        """
        Handle missing values.
        
        Args:
            strategy: 'drop', 'fill_zero', 'fill_mean', or 'fill_mode'
        """
        missing_before = self.df.isnull().sum().sum()
        
        if missing_before == 0:
            return
        
        if strategy == 'drop':
            self.df = self.df.dropna()
            self.cleaning_log.append(f"✓ Dropped rows with missing values")
        
        elif strategy == 'fill_zero':
            self.df = self.df.fillna(0)
            self.cleaning_log.append(f"✓ Filled missing values with 0")
        
        elif strategy == 'fill_mean':
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            self.cleaning_log.append(f"✓ Filled numeric missing values with column means")
        
        elif strategy == 'fill_mode':
            for col in self.df.columns:
                if self.df[col].isnull().any():
                    mode_val = self.df[col].mode()[0] if not self.df[col].mode().empty else None
                    if mode_val is not None:
                        self.df[col] = self.df[col].fillna(mode_val)
            self.cleaning_log.append(f"✓ Filled missing values with column modes")
        
        missing_after = self.df.isnull().sum().sum()
        self.cleaning_log.append(f"  Missing values: {missing_before} → {missing_after}")
    
    def trim_whitespace(self) -> None:
        """Trim whitespace from string columns."""
        string_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(string_cols) > 0:
            for col in string_cols:
                self.df[col] = self.df[col].str.strip() if self.df[col].dtype == 'object' else self.df[col]
            self.cleaning_log.append(f"✓ Trimmed whitespace from {len(string_cols)} text columns")
    
    def convert_data_types(self, type_map: dict = None) -> None:
        """
        Convert columns to specified data types.
        
        Args:
            type_map: Dictionary mapping column names to desired types
                     e.g., {'price': 'float', 'quantity': 'int'}
        """
        if not type_map:
            return
        
        converted = []
        for col, dtype in type_map.items():
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].astype(dtype)
                    converted.append(f"{col} → {dtype}")
                except Exception as e:
                    self.cleaning_log.append(f"⚠ Could not convert {col} to {dtype}: {e}")
        
        if converted:
            self.cleaning_log.append(f"✓ Converted data types: {', '.join(converted)}")
    
    def clean(self, missing_strategy: str = 'drop', type_map: dict = None) -> pd.DataFrame:
        """
        Run all cleaning operations.
        
        Args:
            missing_strategy: Strategy for handling missing values
            type_map: Optional dictionary for data type conversions
            
        Returns:
            Cleaned DataFrame
        """
        if not self.load_data():
            return None
        
        initial_rows = len(self.df)
        
        # Run cleaning steps
        self.standardize_column_names()
        self.trim_whitespace()
        self.remove_duplicates()
        self.handle_missing_values(strategy=missing_strategy)
        
        if type_map:
            self.convert_data_types(type_map)
        
        final_rows = len(self.df)
        
        # Save cleaned data
        self.df.to_csv(self.output_path, index=False)
        self.cleaning_log.append(f"✓ Saved cleaned data to {self.output_path}")
        self.cleaning_log.append(f"✓ Final dataset: {final_rows} rows, {len(self.df.columns)} columns")
        
        return self.df
    
    def print_log(self) -> None:
        """Print cleaning log."""
        print(f"\n{'='*70}")
        print(f"Data Cleaning Report: {self.input_path.name}")
        print(f"{'='*70}")
        for entry in self.cleaning_log:
            print(entry)
        print(f"{'='*70}\n")


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python clean_data.py <input_csv> [output_csv] [missing_strategy]")
        print("\nMissing value strategies: drop, fill_zero, fill_mean, fill_mode")
        print("\nExample:")
        print("  python clean_data.py data/raw/materials.csv")
        print("  python clean_data.py data/raw/materials.csv data/processed/materials.csv drop")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    missing_strategy = sys.argv[3] if len(sys.argv) > 3 else 'drop'
    
    cleaner = DataCleaner(input_path, output_path)
    cleaner.clean(missing_strategy=missing_strategy)
    cleaner.print_log()


if __name__ == "__main__":
    main()
