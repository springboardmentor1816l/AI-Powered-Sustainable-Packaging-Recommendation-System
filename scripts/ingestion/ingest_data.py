"""
PostgreSQL Data Ingestion Script for EcoPackAI
Ingests cleaned CSV files into PostgreSQL database.
"""

import pandas as pd
import sys
from pathlib import Path
from typing import Dict, List
from db_helper import DatabaseHelper


class DataIngestor:
    """Ingests CSV data into PostgreSQL database."""
    
    def __init__(self, db_helper: DatabaseHelper = None):
        """
        Initialize data ingestor.
        
        Args:
            db_helper: DatabaseHelper instance (creates new one if not provided)
        """
        self.db = db_helper or DatabaseHelper()
        self.ingestion_log = []
    
    def ingest_csv(self, 
                   csv_path: str, 
                   table_name: str,
                   column_mapping: Dict[str, str] = None,
                   batch_size: int = 1000) -> bool:
        """
        Ingest CSV file into database table.
        
        Args:
            csv_path: Path to CSV file
            table_name: Target database table name
            column_mapping: Optional dict mapping CSV columns to DB columns
            batch_size: Number of rows to insert per batch
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load CSV
            df = pd.read_csv(csv_path)
            self.ingestion_log.append(f"✓ Loaded {len(df)} rows from {Path(csv_path).name}")
            
            # Check if table exists
            if not self.db.table_exists(table_name):
                self.ingestion_log.append(f"✗ Table '{table_name}' does not exist")
                return False
            
            # Get table schema
            table_info = self.db.get_table_info(table_name)
            db_columns = [col['column_name'] for col in table_info]
            
            # Apply column mapping if provided
            if column_mapping:
                df = df.rename(columns=column_mapping)
            
            # Filter columns to match database schema
            csv_columns = df.columns.tolist()
            valid_columns = [col for col in csv_columns if col in db_columns]
            
            if not valid_columns:
                self.ingestion_log.append(f"✗ No matching columns found between CSV and table")
                return False
            
            # Filter DataFrame to only include valid columns
            df = df[valid_columns]
            
            # Replace NaN with None for proper NULL handling
            df = df.where(pd.notnull(df), None)
            
            # Convert DataFrame to list of tuples
            data = [tuple(row) for row in df.values]
            
            # Insert data in batches
            total_inserted = 0
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                inserted = self.db.bulk_insert(table_name, valid_columns, batch)
                total_inserted += inserted
                
                progress = min(i + batch_size, len(data))
                self.ingestion_log.append(f"  Progress: {progress}/{len(data)} rows")
            
            self.ingestion_log.append(f"✓ Inserted {total_inserted} rows into '{table_name}'")
            return True
            
        except FileNotFoundError:
            self.ingestion_log.append(f"✗ File not found: {csv_path}")
            return False
        except Exception as e:
            self.ingestion_log.append(f"✗ Error during ingestion: {e}")
            return False
    
    def ingest_multiple(self, ingestion_config: List[Dict]) -> Dict[str, bool]:
        """
        Ingest multiple CSV files based on configuration.
        
        Args:
            ingestion_config: List of dicts with keys: csv_path, table_name, column_mapping
            
        Returns:
            Dictionary mapping table names to success status
        """
        results = {}
        
        for config in ingestion_config:
            csv_path = config['csv_path']
            table_name = config['table_name']
            column_mapping = config.get('column_mapping', None)
            
            self.ingestion_log.append(f"\n{'='*70}")
            self.ingestion_log.append(f"Ingesting: {table_name}")
            self.ingestion_log.append(f"{'='*70}")
            
            success = self.ingest_csv(csv_path, table_name, column_mapping)
            results[table_name] = success
        
        return results
    
    def verify_ingestion(self, table_name: str, expected_count: int = None) -> bool:
        """
        Verify that data was ingested correctly.
        
        Args:
            table_name: Name of the table to verify
            expected_count: Expected number of rows (optional)
            
        Returns:
            True if verification passed, False otherwise
        """
        try:
            # Get actual row count
            query = f"SELECT COUNT(*) FROM {table_name}"
            result = self.db.execute_query(query)
            actual_count = result[0][0] if result else 0
            
            self.ingestion_log.append(f"\nVerification for '{table_name}':")
            self.ingestion_log.append(f"  Rows in table: {actual_count}")
            
            if expected_count is not None:
                if actual_count == expected_count:
                    self.ingestion_log.append(f"  ✓ Count matches expected: {expected_count}")
                    return True
                else:
                    self.ingestion_log.append(f"  ✗ Count mismatch! Expected: {expected_count}")
                    return False
            
            return True
            
        except Exception as e:
            self.ingestion_log.append(f"  ✗ Verification failed: {e}")
            return False
    
    def print_log(self) -> None:
        """Print ingestion log."""
        print("\n")
        for entry in self.ingestion_log:
            print(entry)
        print("\n")


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 3:
        print("Usage: python ingest_data.py <csv_file> <table_name>")
        print("\nExample:")
        print("  python ingest_data.py data/processed/materials.csv materials")
        print("  python ingest_data.py data/processed/products.csv products")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    table_name = sys.argv[2]
    
    # Test database connection first
    db = DatabaseHelper()
    if not db.test_connection():
        print("\n✗ Could not connect to database!")
        print("Please check database connection settings.")
        sys.exit(1)
    
    # Create ingestor and run
    ingestor = DataIngestor(db)
    success = ingestor.ingest_csv(csv_path, table_name)
    ingestor.print_log()
    
    if success:
        # Verify ingestion
        ingestor.verify_ingestion(table_name)
        ingestor.print_log()
        print("✓ Ingestion completed successfully!")
    else:
        print("✗ Ingestion failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
