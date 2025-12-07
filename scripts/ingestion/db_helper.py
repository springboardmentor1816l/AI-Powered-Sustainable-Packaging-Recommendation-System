"""
Database Helper for EcoPackAI
Provides database connection utilities and helper functions.
"""

import psycopg2
from psycopg2 import sql, extras
import os
from typing import Dict, List, Optional
from contextlib import contextmanager


class DatabaseHelper:
    """Helper class for PostgreSQL database operations."""
    
    def __init__(self, 
                 dbname: str = None,
                 user: str = None,
                 password: str = None,
                 host: str = None,
                 port: str = None):
        """
        Initialize database connection parameters.
        
        Args:
            dbname: Database name (defaults to env var DB_NAME or 'ecopackai_db')
            user: Database user (defaults to env var DB_USER or 'postgres')
            password: Database password (defaults to env var DB_PASSWORD)
            host: Database host (defaults to env var DB_HOST or 'localhost')
            port: Database port (defaults to env var DB_PORT or '5432')
        """
        self.dbname = dbname or os.getenv('DB_NAME', 'ecopackai_db')
        self.user = user or os.getenv('DB_USER', 'postgres')
        self.password = password or os.getenv('DB_PASSWORD', '')
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.port = port or os.getenv('DB_PORT', '5432')
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            psycopg2 connection object
        """
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            yield conn
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"✓ Connected to PostgreSQL: {version[0]}")
                return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL query string
            params: Optional query parameters
            
        Returns:
            List of result tuples
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_command(self, command: str, params: tuple = None) -> int:
        """
        Execute an INSERT/UPDATE/DELETE command.
        
        Args:
            command: SQL command string
            params: Optional command parameters
            
        Returns:
            Number of rows affected
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(command, params)
            conn.commit()
            return cursor.rowcount
    
    def bulk_insert(self, table_name: str, columns: List[str], data: List[tuple]) -> int:
        """
        Bulk insert data into a table.
        
        Args:
            table_name: Name of the table
            columns: List of column names
            data: List of tuples containing row data
            
        Returns:
            Number of rows inserted
        """
        if not data:
            return 0
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build INSERT query
            cols = sql.SQL(', ').join(map(sql.Identifier, columns))
            placeholders = sql.SQL(', ').join(sql.Placeholder() * len(columns))
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                cols,
                placeholders
            )
            
            # Execute bulk insert
            extras.execute_batch(cursor, query, data)
            conn.commit()
            
            return cursor.rowcount
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists, False otherwise
        """
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """
        result = self.execute_query(query, (table_name,))
        return result[0][0] if result else False
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """
        Get column information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of dictionaries containing column info
        """
        query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s
            ORDER BY ordinal_position;
        """
        
        results = self.execute_query(query, (table_name,))
        
        return [
            {
                'column_name': row[0],
                'data_type': row[1],
                'is_nullable': row[2],
                'default': row[3]
            }
            for row in results
        ]
    
    def get_row_count(self, table_name: str) -> int:
        """
        Get the number of rows in a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Number of rows
        """
        query = sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table_name))
        result = self.execute_query(query.as_string(psycopg2.connect(
            dbname=self.dbname, user=self.user, password=self.password,
            host=self.host, port=self.port
        )))
        return result[0][0] if result else 0
    
    def truncate_table(self, table_name: str) -> None:
        """
        Truncate a table (remove all rows).
        
        Args:
            table_name: Name of the table
        """
        command = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE").format(
            sql.Identifier(table_name)
        )
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(command)
            conn.commit()
            print(f"✓ Truncated table '{table_name}'")


def main():
    """Test database connection."""
    print("Testing database connection...")
    db = DatabaseHelper()
    
    if db.test_connection():
        print("\n✓ Database connection successful!")
        
        # List available tables
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """
        
        try:
            tables = db.execute_query(query)
            if tables:
                print(f"\nAvailable tables ({len(tables)}):")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("\nNo tables found in database.")
        except Exception as e:
            print(f"\nCould not list tables: {e}")
    else:
        print("\n✗ Database connection failed!")
        print("\nPlease check:")
        print("  1. PostgreSQL is running")
        print("  2. Database credentials are correct")
        print("  3. Database exists")
        print("\nSet environment variables or edit db_helper.py:")
        print("  DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT")


if __name__ == "__main__":
    main()
