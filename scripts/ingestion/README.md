# EcoPackAI Scripts

This directory contains utility scripts for data processing, database management, and system operations.

## 📁 Directory Structure

```
scripts/
└── ingestion/
    ├── validate_csv.py          # CSV validation and quality checks
    ├── clean_data.py             # Data cleaning and standardization
    ├── db_helper.py              # Database connection utilities
    ├── ingest_data.py            # PostgreSQL data ingestion
    ├── batch_import.py           # Batch processing for multiple datasets
    └── README.md                 # This file
```

---

## 🔧 Script Descriptions

### 1. validate_csv.py

**Purpose**: Validate CSV files for schema consistency, data quality, and completeness.

**Features**:
- Check for missing values
- Detect duplicate rows
- Validate column naming conventions
- Verify data types
- Check against expected schema

**Usage**:
```bash
# Basic validation
python scripts/ingestion/validate_csv.py data/raw_datasets/materials/raw_materials.csv

# Validate with expected columns
python scripts/ingestion/validate_csv.py data/raw_datasets/materials/raw_materials.csv '["material_id","material_type","cost_per_kg"]'
```

**Output**:
- Console validation report
- Status: PASSED / PASSED_WITH_WARNINGS / FAILED
- Detailed issues and warnings

---

### 2. clean_data.py

**Purpose**: Clean and standardize CSV files for database ingestion.

**Features**:
- Standardize column names to snake_case
- Remove duplicate rows
- Handle missing values (multiple strategies)
- Trim whitespace from text columns
- Convert data types

**Usage**:
```bash
# Basic cleaning (drops rows with missing values)
python scripts/ingestion/clean_data.py data/raw_datasets/materials/raw_materials.csv

# Specify output path
python scripts/ingestion/clean_data.py data/raw_datasets/materials/raw_materials.csv data/processed/materials.csv

# Use different missing value strategy
python scripts/ingestion/clean_data.py data/raw_datasets/materials/raw_materials.csv data/processed/materials.csv fill_mean
```

**Missing Value Strategies**:
- `drop`: Remove rows with any missing values
- `fill_zero`: Fill missing values with 0
- `fill_mean`: Fill numeric columns with mean
- `fill_mode`: Fill columns with mode (most frequent value)

**Output**:
- Cleaned CSV file in `data/processed/` directory
- Cleaning log with actions performed

---

### 3. db_helper.py

**Purpose**: Database connection utilities and helper functions.

**Features**:
- Connection management with context managers
- Test database connectivity
- Execute queries and commands
- Bulk insert operations
- Table information retrieval

**Usage**:
```bash
# Test database connection
python scripts/ingestion/db_helper.py
```

**As a Module**:
```python
from scripts.ingestion.db_helper import DatabaseHelper

db = DatabaseHelper()

# Test connection
db.test_connection()

# Execute query
results = db.execute_query("SELECT * FROM materials LIMIT 10")

# Bulk insert
data = [(1, 'Cardboard', 0.45), (2, 'Plastic', 1.20)]
db.bulk_insert('materials', ['id', 'type', 'cost'], data)
```

**Environment Variables** (optional):
- `DB_NAME`: Database name (default: ecopackai_db)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 5432)

---

### 4. ingest_data.py

**Purpose**: Ingest cleaned CSV files into PostgreSQL database.

**Features**:
- CSV to PostgreSQL import
- Column mapping support
- Batch processing
- Automatic schema validation
- Ingestion verification

**Usage**:
```bash
# Ingest single CSV file
python scripts/ingestion/ingest_data.py data/processed/materials.csv materials

# Ingest products
python scripts/ingestion/ingest_data.py data/processed/products.csv products
```

**Prerequisites**:
- Database must be running
- Tables must exist (create schema first)
- CSV columns must match database schema

**Output**:
- Progress log
- Rows inserted count
- Verification results

---

### 5. batch_import.py

**Purpose**: Automate ingestion of multiple datasets using configuration file.

**Features**:
- Multi-dataset processing
- Automated validation, cleaning, and ingestion
- YAML/JSON configuration support
- Batch processing summary

**Usage**:
```bash
# Create sample configuration
python scripts/ingestion/batch_import.py --create-config batch_config.yaml

# Run batch import
python scripts/ingestion/batch_import.py batch_config.yaml
```

**Configuration File Example** (`batch_config.yaml`):
```yaml
datasets:
  - csv_path: data/raw_datasets/materials/materials.csv
    table_name: materials
    output_path: data/processed/materials.csv
    missing_strategy: drop
    expected_columns:
      - material_id
      - material_type
      - cost_per_kg
    column_mapping: null
  
  - csv_path: data/raw_datasets/products/products.csv
    table_name: products
    output_path: data/processed/products.csv
    missing_strategy: drop
    expected_columns:
      - product_id
      - product_name
      - category
```

**Output**:
- Validation reports for all datasets
- Cleaning logs
- Ingestion results
- Summary table

---

## 🚀 Complete Workflow

### Step 1: Collect Raw Datasets
Place raw CSV files in appropriate subdirectories:
```
data/raw_datasets/
├── materials/
│   └── raw_materials.csv
├── products/
│   └── raw_products.csv
├── sustainability/
│   └── sustainability_metrics.csv
└── financial/
    └── cost_data.csv
```

### Step 2: Validate Raw Data
```bash
python scripts/ingestion/validate_csv.py data/raw_datasets/materials/raw_materials.csv
```

Review validation report and address any critical issues.

### Step 3: Clean Data
```bash
python scripts/ingestion/clean_data.py data/raw_datasets/materials/raw_materials.csv
```

Cleaned file will be saved to `data/processed/cleaned_raw_materials.csv`.

### Step 4: Test Database Connection
```bash
python scripts/ingestion/db_helper.py
```

Ensure database is accessible and schema exists.

### Step 5: Ingest Data
```bash
python scripts/ingestion/ingest_data.py data/processed/cleaned_raw_materials.csv materials
```

### Alternative: Batch Processing

For multiple datasets, use batch import:

```bash
# Create config
python scripts/ingestion/batch_import.py --create-config my_import.yaml

# Edit my_import.yaml with your dataset paths

# Run batch import
python scripts/ingestion/batch_import.py my_import.yaml
```

---

## 📊 Data Pipeline Diagram

```
Raw CSV Files
     ↓
[validate_csv.py] ─→ Validation Report
     ↓
[clean_data.py] ─→ Cleaned CSV
     ↓
[ingest_data.py] ─→ PostgreSQL Database
     ↓
Verification & Reports
```

---

## 🔍 Troubleshooting

### Issue: "Database connection failed"
**Solution**:
1. Check if PostgreSQL is running
2. Verify database credentials
3. Ensure database exists
4. Set environment variables or edit `db_helper.py`

### Issue: "Table does not exist"
**Solution**:
1. Run database schema creation first:
   ```bash
   psql -U postgres -d ecopackai_db -f backend/db/schema.sql
   ```

### Issue: "Column mismatch"
**Solution**:
1. Check CSV columns match database schema
2. Use column_mapping in batch_import config
3. Ensure clean_data.py standardized column names

### Issue: "Too many missing values"
**Solution**:
1. Review raw dataset quality
2. Choose appropriate missing value strategy
3. Consider data imputation or finding better source

---

## 📝 Best Practices

1. **Always validate before cleaning**: Run `validate_csv.py` first
2. **Keep raw data intact**: Never modify files in `raw_datasets/`
3. **Document sources**: Create `dataset_info.txt` for each raw dataset
4. **Use batch processing**: For multiple datasets, use `batch_import.py`
5. **Verify ingestion**: Check row counts and sample queries after import
6. **Version control**: Commit configuration files but not data files

---

## 📦 Dependencies

Required Python packages:
```
pandas
psycopg2-binary
pyyaml (for batch_import.py)
```

Install dependencies:
```bash
pip install pandas psycopg2-binary pyyaml
```

---

## 🔗 Related Documentation

- [Dataset Sourcing Guide](../../docs/dataset_sourcing_guide.md)
- [Data Validation Report Template](../../docs/data_validation_report.md)
- [Database Schema Documentation](../../docs/data_dictionary.md)
- [Main Data README](../../data/README.md)

---

## 💡 Tips

- Use `--help` flag on any script for more options (future enhancement)
- For large datasets (>100k rows), increase batch_size in `ingest_data.py`
- Enable logging for production use
- Consider using TimescaleDB extensions for time-series data

---

**Last Updated**: 2025-12-07  
**Maintained By**: EcoPackAI Development Team
