# Dataset Sourcing Guide for EcoPackAI

This guide provides comprehensive information on sourcing publicly available datasets for packaging materials, products, sustainability metrics, and financial data.

## 📌 Overview

The EcoPackAI project requires diverse datasets covering:
- **Packaging materials** (specifications, properties, costs)
- **Product information** (dimensions, weights, fragility)
- **Sustainability metrics** (recyclability, CO2 emissions, lifecycle data)
- **Financial data** (material costs, market trends)

---

## 🔍 Recommended Data Sources

### 1. Kaggle

**URL**: [https://www.kaggle.com/datasets](https://www.kaggle.com/datasets)

**Relevant Dataset Categories**:
- Environmental & Sustainability
- Business & Economics
- Manufacturing & Industrial

**Search Keywords**:
- "packaging materials"
- "sustainability index"
- "recycling data"
- "carbon footprint"
- "product specifications"
- "eco-friendly materials"

**How to Download**:
1. Create a free Kaggle account
2. Search for relevant datasets
3. Click "Download" button
4. Extract CSV files

**Recommended Datasets** (as of 2024):
- Sustainable Packaging Materials Database
- Product Carbon Footprint Data
- Recycling & Waste Management Statistics

---

### 2. Government Environmental Databases

#### EPA (Environmental Protection Agency) - USA
**URL**: [https://www.epa.gov/data](https://www.epa.gov/data)

**Datasets**:
- Greenhouse Gas Emissions Data
- Waste Reduction Model (WARM)
- Sustainable Materials Management Data

#### European Environment Agency (EEA)
**URL**: [https://www.eea.europa.eu/data-and-maps](https://www.eea.europa.eu/data-and-maps)

**Datasets**:
- Waste statistics
- Packaging waste data
- Circular economy indicators

#### India - Ministry of Environment, Forest and Climate Change
**URL**: [https://moef.gov.in/](https://moef.gov.in/)

**Datasets**:
- E-waste management data
- Plastic waste management statistics

---

### 3. Research Repositories

#### IEEE DataPort
**URL**: [https://ieee-dataport.org/](https://ieee-dataport.org/)

**Topics**:
- Materials science datasets
- Industrial IoT sensor data
- Sustainability research data

#### ScienceDirect (Elsevier)
**URL**: [https://www.sciencedirect.com/](https://www.sciencedirect.com/)

**Access**:
- Many research papers include supplementary datasets
- Look for "Data availability" sections
- Some datasets available via Data in Brief journal

#### Zenodo
**URL**: [https://zenodo.org/](https://zenodo.org/)

**Benefits**:
- Open-access research data repository
- DOI for each dataset
- Search for "packaging", "sustainability", "lifecycle assessment"

---

### 4. Industry & Commercial Sources

#### Material Properties Databases

**MatWeb** - [http://www.matweb.com/](http://www.matweb.com/)
- Free material property data
- Plastics, metals, composites
- Can export data for common materials

**Granta Design (Ansys)** - Limited free access
- Material selection databases
- Environmental impact data

#### Packaging Industry Associations

**Sustainable Packaging Coalition**
- [https://sustainablepackaging.org/](https://sustainablepackaging.org/)
- Industry reports and whitepapers
- Some data available publicly

**World Packaging Organisation**
- [http://www.worldpackaging.org/](http://www.worldpackaging.org/)
- Global packaging statistics

---

### 5. Open Data Portals

#### Data.gov (USA)
**URL**: [https://data.gov/](https://data.gov/)

**Search for**:
- "packaging"
- "recycling"
- "materials"
- "sustainability"

#### EU Open Data Portal
**URL**: [https://data.europa.eu/](https://data.europa.eu/)

**Categories**:
- Environment
- Economy and finance
- Industry

#### UK Government Data
**URL**: [https://data.gov.uk/](https://data.gov.uk/)

---

## 📦 Dataset Categories to Collect

### 1. Materials Dataset

**Required Columns**:
- `material_id` or `material_name`
- `material_type` (cardboard, plastic, bioplastic, etc.)
- `density` (g/cm³)
- `strength_mpa` (Megapascals)
- `weight_capacity` (kg)
- `biodegradability_percent`
- `co2_emission_score`
- `recyclability_percent`
- `cost_per_kg`
- `industry_use_case`

**Suggested Sources**:
- MatWeb (material properties)
- EPA WARM tool (environmental metrics)
- Kaggle sustainability datasets

---

### 2. Products Dataset

**Required Columns**:
- `product_id`
- `product_name`
- `category` (electronics, food, cosmetics, pharmacy)
- `product_weight` (kg)
- `dimensions` (length, width, height in cm)
- `volume` (cm³)
- `fragility_index` (1-10 scale)
- `shipping_type` (standard, express, fragile)

**Suggested Sources**:
- E-commerce product catalogs (Amazon, eBay datasets)
- Manufacturing industry reports
- Create synthetic data based on real product specifications

---

### 3. Sustainability Indexes

**Required Columns**:
- `material_name`
- `recycling_rate` (%)
- `lifecycle_co2_emissions` (kg CO2e)
- `water_usage` (liters)
- `energy_consumption` (kWh)
- `end_of_life_score`
- `sustainability_rating` (A-F or 1-100)

**Suggested Sources**:
- Life Cycle Assessment (LCA) databases
- EEA circular economy data
- Academic research papers

---

### 4. Financial/Cost Data

**Required Columns**:
- `material_name`
- `cost_per_kg` or `cost_per_unit`
- `market_price_trend` (increasing/stable/decreasing)
- `availability_score`
- `supplier_region`

**Suggested Sources**:
- Industry market reports
- Trading platforms (plastics, paper markets)
- Government commerce statistics

---

## 🛠️ Data Collection Workflow

### Step 1: Identify Dataset
1. Search recommended sources
2. Review dataset description and schema
3. Check data quality and completeness
4. Verify licensing (must be public/open data)

### Step 2: Download Raw Data
1. Download CSV/Excel files
2. Save to `/data/raw_datasets/<category>` directory
3. Document source URL and download date

### Step 3: Initial Assessment
Use validation script:
```bash
python scripts/ingestion/validate_csv.py data/raw_datasets/materials/raw_materials.csv
```

### Step 4: Document Dataset
Create a metadata file (`dataset_info.txt`) with:
- Source URL
- Download date
- License information
- Column descriptions
- Known issues/limitations

---

## 📝 Dataset Templates

### Materials Template
```csv
material_id,material_type,strength_mpa,weight_capacity,biodegradability_percent,co2_emission_score,recyclability_percent,cost_per_kg,industry_use_case
1,Recycled Cardboard,5.5,25,85,3.2,95,0.45,Electronics
2,Bioplastic PLA,48,15,90,2.8,70,2.15,Food
3,Mushroom Packaging,3.0,10,100,1.5,85,3.80,Fragile Items
```

### Products Template
```csv
product_id,product_name,category,product_weight,fragility_index,shipping_type
1,Smartphone,Electronics,0.2,8,Fragile
2,Laptop,Electronics,2.5,7,Standard
3,Organic Coffee,Food,0.5,3,Standard
```

---

## ⚠️ Data Quality Checklist

Before using any dataset:

- [ ] **Licensing**: Confirm data is public/open-source
- [ ] **Completeness**: Check for excessive missing values (<10% preferred)
- [ ] **Accuracy**: Cross-reference with known standards
- [ ] **Relevance**: Ensure data matches project requirements
- [ ] **Recency**: Prefer datasets updated within last 2 years
- [ ] **Format**: CSV format preferred, convertible to CSV acceptable
- [ ] **Documentation**: Source has clear column definitions
- [ ] **Size**: Minimum 100 rows for meaningful analysis

---

## 🔗 Quick Reference Links

| Source Type | Primary Link | Best For |
|------------|-------------|----------|
| Kaggle | [kaggle.com/datasets](https://kaggle.com/datasets) | General datasets |
| EPA | [epa.gov/data](https://epa.gov/data) | Environmental data |
| EEA | [eea.europa.eu](https://eea.europa.eu) | EU environmental data |
| Data.gov | [data.gov](https://data.gov) | US government data |
| Zenodo | [zenodo.org](https://zenodo.org) | Research data |
| MatWeb | [matweb.com](http://matweb.com) | Material properties |

---

## 💡 Tips for Dataset Sourcing

1. **Start with Kaggle**: Easiest to find preprocessed datasets
2. **Check licenses**: Ensure commercial use is allowed
3. **Combine sources**: Merge data from multiple sources for completeness
4. **Document everything**: Keep track of sources for reproducibility
5. **Version control**: Save original raw files before any modifications
6. **Validate early**: Run validation scripts before extensive cleaning

---

## 📧 Need Help?

If you cannot find specific datasets:
1. Check academic papers in your domain - many include supplementary data
2. Consider creating synthetic data based on industry standards
3. Reach out to packaging industry associations
4. Use open APIs (e.g., World Bank API for economic data)

---

**Next Steps**: After collecting datasets, proceed to:
1. Validation using `validate_csv.py`
2. Cleaning using `clean_data.py`
3. Ingestion using `ingest_data.py` or `batch_import.py`
