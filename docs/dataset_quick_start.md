# Dataset Preparation Quick Start Guide

Welcome to the EcoPackAI dataset preparation workflow! This guide will help you get started with collecting, validating, cleaning, and ingesting datasets.

---

## 🚀 Quick Start (5 Steps)

### Step 1: Install Dependencies

```bash
pip install pandas psycopg2-binary pyyaml
```

### Step 2: Set Up Database

Ensure PostgreSQL is running and create the database:

```bash
# Create database (if not exists)
createdb ecopackai_db

# Run schema
psql -U postgres -d ecopackai_db -f backend/db/schema.sql
```

### Step 3: Test Database Connection

```bash
python scripts/ingestion/db_helper.py
```

You should see: `✓ Connected to PostgreSQL`

### Step 4: Use Sample Data (Quick Demo)

```bash
# Validate sample data
python scripts/ingestion/validate_csv.py data/raw_datasets/materials/sample_materials_template.csv

# Clean sample data
python scripts/ingestion/clean_data.py data/raw_datasets/materials/sample_materials_template.csv

# Ingest into database (ensure materials table exists)
python scripts/ingestion/ingest_data.py data/processed/cleaned_sample_materials_template.csv materials
```

### Step 5: Source Real Datasets

Follow the [Dataset Sourcing Guide](docs/dataset_sourcing_guide.md) to find and download real datasets from Kaggle, EPA, and other sources.

---

## 📋 Complete Workflow

### Phase 1: Dataset Acquisition

1. **Review sourcing guide**: `docs/dataset_sourcing_guide.md`
2. **Download datasets** from recommended sources
3. **Save to appropriate directory**:
   ```
   data/raw_datasets/
   ├── materials/
   ├── products/
   ├── sustainability/
   └── financial/
   ```
4. **Document sources**: Create `dataset_info.txt` with source URL and date

### Phase 2: Validation

```bash
# Validate each dataset
python scripts/ingestion/validate_csv.py data/raw_datasets/materials/your_dataset.csv

# Review validation report
# Fix critical issues before proceeding
```

### Phase 3: Cleaning

```bash
# Clean data with appropriate strategy
python scripts/ingestion/clean_data.py data/raw_datasets/materials/your_dataset.csv data/processed/materials.csv drop

# Options for missing value handling:
# drop, fill_zero, fill_mean, fill_mode
```

### Phase 4: Ingestion

```bash
# Single dataset ingestion
python scripts/ingestion/ingest_data.py data/processed/materials.csv materials

# Or use batch import for multiple datasets
python scripts/ingestion/batch_import.py --create-config my_import.yaml
# Edit my_import.yaml
python scripts/ingestion/batch_import.py my_import.yaml
```

### Phase 5: Verification & Documentation

```bash
# Query database to verify
psql -U postgres -d ecopackai_db -c "SELECT COUNT(*) FROM materials;"

# Fill out validation report
# Edit: docs/data_validation_report.md
```

---

## 🎯 Directory Structure

After setup, your structure should look like:

```
EcopackAI/
├── data/
│   ├── raw_datasets/          # Original downloaded CSVs
│   │   ├── materials/
│   │   ├── products/
│   │   ├── sustainability/
│   │   └── financial/
│   ├── processed/             # Cleaned, ingest-ready CSVs
│   ├── material_dataset.csv   # Sample data (existing)
│   └── product_dataset.csv    # Sample data (existing)
├── scripts/
│   └── ingestion/
│       ├── validate_csv.py
│       ├── clean_data.py
│       ├── db_helper.py
│       ├── ingest_data.py
│       ├── batch_import.py
│       └── README.md
├── docs/
│   ├── dataset_sourcing_guide.md
│   ├── data_validation_report.md
│   └── data_dictionary.md
```

---

## 🛠️ Common Commands

### Validation
```bash
# Basic validation
python scripts/ingestion/validate_csv.py <csv_path>

# With expected columns
python scripts/ingestion/validate_csv.py <csv_path> '["col1","col2","col3"]'
```

### Cleaning
```bash
# Auto output to processed/
python scripts/ingestion/clean_data.py <input_csv>

# Specify output
python scripts/ingestion/clean_data.py <input_csv> <output_csv>

# With strategy
python scripts/ingestion/clean_data.py <input_csv> <output_csv> fill_mean
```

### Ingestion
```bash
# Single file
python scripts/ingestion/ingest_data.py <csv_path> <table_name>

# Batch import
python scripts/ingestion/batch_import.py <config_file>
```

### Database Checks
```bash
# Test connection
python scripts/ingestion/db_helper.py

# Check tables
psql -U postgres -d ecopackai_db -c "\dt"

# Count rows
psql -U postgres -d ecopackai_db -c "SELECT COUNT(*) FROM materials;"
```

---

## 🔧 Configuration

### Database Credentials

Set environment variables (optional):

```bash
# Windows PowerShell
$env:DB_NAME="ecopackai_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"

# Or edit db_helper.py directly
```

### Batch Import Config

Create `batch_import_config.yaml`:

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
```

---

## 📊 Sample Dataset Templates

We've provided sample templates in `data/raw_datasets/`:

- **Materials**: `materials/sample_materials_template.csv`
- **Products**: `products/sample_products_template.csv`
- **Sustainability**: `sustainability/sample_sustainability_template.csv`

Use these as references for expected data formats.

---

## ⚠️ Common Issues

### Issue: ModuleNotFoundError

**Solution**:
```bash
pip install pandas psycopg2-binary pyyaml
```

### Issue: Database connection failed

**Solutions**:
1. Check if PostgreSQL is running: `pg_ctl status`
2. Verify credentials in environment variables
3. Ensure database exists: `psql -l`

### Issue: Table does not exist

**Solution**:
```bash
psql -U postgres -d ecopackai_db -f backend/db/schema.sql
```

### Issue: Permission denied

**Solution**:
- Check file paths are correct
- Ensure you have write permissions for directories
- On Windows, avoid special characters in paths

---

## 📚 Documentation Links

- **[Dataset Sourcing Guide](docs/dataset_sourcing_guide.md)**: Where to find datasets
- **[Scripts README](scripts/ingestion/README.md)**: Detailed script documentation
- **[Validation Report Template](docs/data_validation_report.md)**: Report format
- **[Database Schema](docs/data_dictionary.md)**: Table definitions

---

## ✅ Checklist

Before starting:
- [ ] PostgreSQL installed and running
- [ ] Python dependencies installed
- [ ] Database schema created
- [ ] Database connection tested

During workflow:
- [ ] Datasets downloaded and documented
- [ ] Validation passed for all datasets
- [ ] Data cleaned and saved to processed/
- [ ] Data ingested successfully
- [ ] Row counts verified
- [ ] Validation report completed

---

## 💡 Tips

1. **Start small**: Test with sample data first
2. **Document sources**: Always note where data came from
3. **Version control**: Commit scripts and configs, not data files
4. **Review validation**: Don't skip the validation step
5. **Keep raw data**: Never modify original raw datasets
6. **Use batch mode**: For multiple datasets, use `batch_import.py`

---

## 🎓 Learning Path

1. ✅ Run quick start with sample data
2. ✅ Download one real dataset from Kaggle
3. ✅ Practice validation → cleaning → ingestion
4. ✅ Create batch import config for multiple datasets
5. ✅ Complete validation report
6. ✅ Share with team for review

---

## 📞 Need Help?

- Review script documentation: `scripts/ingestion/README.md`
- Check troubleshooting section in scripts README
- Verify all prerequisites are met
- Ensure database schema matches your data

---

**Happy data wrangling!** 🎉

*Last updated: 2025-12-07*
