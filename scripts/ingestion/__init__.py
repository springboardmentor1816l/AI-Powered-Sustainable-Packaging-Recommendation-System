"""
Data ingestion package for EcoPackAI.

This package provides utilities for CSV validation, data cleaning,
and PostgreSQL database ingestion.
"""

__version__ = '1.0.0'
__author__ = 'EcoPackAI Development Team'

from .db_helper import DatabaseHelper
from .ingest_data import DataIngestor
from .validate_csv import CSVValidator
from .clean_data import DataCleaner

__all__ = [
    'DatabaseHelper',
    'DataIngestor',
    'CSVValidator',
    'DataCleaner',
]
