"""
scripts/cleaning/ingestion_data.py

Robust, idempotent cleaning script to transform raw CSVs into ingestion-ready CSVs.
Reads:
  - data/raw_datasets/material_dataset_raw.csv
  - data/raw_datasets/product_dataset_raw.csv
Writes:
  - data/processed/material_dataset.csv
  - data/processed/product_dataset.csv

The script is defensive about column name variants, numeric parsing, and uses medians/modes for imputation.
It is safe to run multiple times (idempotent) and will overwrite processed files.
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]  # repo root (/mnt/data)
RAW = BASE / "data" / "raw_datasets"
PROCESSED = BASE / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

def robust_snake(col):
    s = str(col).strip().lower()
    s = re.sub(r'[^0-9a-z]+', '_', s)
    s = re.sub(r'_{2,}', '_', s)
    s = s.strip('_')
    return s

def parse_numeric_val(s):
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    if s == '' or s.lower() in ['nan', 'none', 'null']:
        return np.nan
    # remove commas and common text
    s = s.replace(',', ' ')
    # remove currency words/symbols and units
    s = re.sub(r'(?i)rs\.?\s*', '', s)
    s = re.sub(r'(?i)inr\.?\s*', '', s)
    s = re.sub(r'(?i)per\s*kg', '', s)
    s = re.sub(r'(?i)kg\b', '', s)
    s = re.sub(r'(?i)approx\s*', '', s)
    # keep digits, dot, minus
    m = re.search(r'[-+]?\d*\.?\d+', s)
    if m:
        try:
            return float(m.group(0))
        except:
            return np.nan
    return np.nan

def parse_boolean(s):
    if pd.isna(s):
        return np.nan
    s = str(s).strip().lower()
    if s in ['true','t','yes','y','1']:
        return True
    if s in ['false','f','no','n','0','']:
        return False
    return np.nan

def map_material_cols(cols):
    mapped = {}
    for c in cols:
        s = robust_snake(c)
        if 'material' in s and 'id' in s:
            mapped[c] = 'material_id'
        elif 'material' in s and 'type' in s:
            mapped[c] = 'material_type'
        elif 'strength' in s:
            mapped[c] = 'strength_mpa'
        elif 'weight' in s and 'capacity' in s:
            mapped[c] = 'weight_capacity'
        elif 'biodegrad' in s:
            mapped[c] = 'biodegradability_percent'
        elif 'co2' in s or 'co2_emission' in s or 'co2emission' in s:
            mapped[c] = 'co2_emission_score'
        elif 'recycl' in s:
            mapped[c] = 'recyclability_percent'
        elif 'cost' in s and 'kg' in s:
            mapped[c] = 'cost_per_kg'
        elif 'industry' in s or 'use' in s or 'case' in s:
            mapped[c] = 'industry_use_case'
        elif 'upload' in s and 'time' in s:
            mapped[c] = 'upload_timestamp'
        else:
            mapped[c] = c
    return mapped

def map_product_cols(cols):
    mapped = {}
    for c in cols:
        s = robust_snake(c)
        if 'product' in s and 'id' in s:
            mapped[c] = 'product_id'
        elif ('product' in s and 'name' in s) or 'product_name' in s:
            mapped[c] = 'product_name'
        elif 'category' in s:
            mapped[c] = 'category'
        elif 'weight' in s:
            mapped[c] = 'product_weight'
        elif 'fragility' in s:
            mapped[c] = 'fragility_index'
        elif 'ship' in s or 'shipping' in s:
            mapped[c] = 'shipping_type'
        elif 'active' in s:
            mapped[c] = 'is_active'
        else:
            mapped[c] = c
    return mapped

def clean_materials(raw_path, out_path, reference_clean_path=None):
    df = pd.read_csv(raw_path, dtype=str)
    col_map = map_material_cols(df.columns)
    df = df.rename(columns=col_map)

    # Ensure expected columns exist
    expected = ['material_id','material_type','strength_mpa','weight_capacity','biodegradability_percent',
                'co2_emission_score','recyclability_percent','cost_per_kg','industry_use_case','upload_timestamp']
    for c in expected:
        if c not in df.columns:
            df[c] = np.nan

    # Text normalization
    df['material_type'] = df['material_type'].astype(str).str.strip()
    df['industry_use_case'] = df['industry_use_case'].astype(str).replace('nan','', regex=False)
    df['industry_use_case'] = df['industry_use_case'].str.replace(',', ';')
    df['industry_use_case'] = df['industry_use_case'].str.replace(r'\s*;\s*', ';', regex=True)
    df['industry_use_case'] = df['industry_use_case'].str.strip().str.lower().replace('', np.nan)

    # Parse numerics
    for col in ['strength_mpa','weight_capacity','biodegradability_percent','co2_emission_score','recyclability_percent','cost_per_kg']:
        df[col] = df[col].apply(parse_numeric_val)

    # Parse timestamp if present
    if 'upload_timestamp' in df.columns:
        df['upload_timestamp'] = pd.to_datetime(df['upload_timestamp'], errors='coerce')

    # material_id numeric
    df['material_id'] = pd.to_numeric(df['material_id'], errors='coerce').astype('Int64')

    # Drop exact duplicates
    df = df.drop_duplicates()

    # Remove rows missing material_type
    df = df[~df['material_type'].isna()]

    # For imputation, if reference_clean_path provided, use medians from it; else use current medians
    if reference_clean_path and Path(reference_clean_path).exists():
        ref = pd.read_csv(reference_clean_path)
        medians = {col: float(ref[col].median()) if col in ref.columns else 0.0 for col in ['strength_mpa','weight_capacity','biodegradability_percent','co2_emission_score','recyclability_percent','cost_per_kg']}
    else:
        medians = {col: float(df[col].median()) if df[col].notna().sum()>0 else 0.0 for col in ['strength_mpa','weight_capacity','biodegradability_percent','co2_emission_score','recyclability_percent','cost_per_kg']}

    for col, med in medians.items():
        df[col] = df[col].fillna(med)

    # Ensure types
    df['strength_mpa'] = df['strength_mpa'].astype(float)
    df['weight_capacity'] = df['weight_capacity'].astype(float)
    df['biodegradability_percent'] = df['biodegradability_percent'].astype(float)
    df['co2_emission_score'] = df['co2_emission_score'].astype(float)
    df['recyclability_percent'] = df['recyclability_percent'].astype(float)
    df['cost_per_kg'] = df['cost_per_kg'].astype(float)

    # Reorder and write
    out = df[['material_id','material_type','strength_mpa','weight_capacity','biodegradability_percent','co2_emission_score','recyclability_percent','cost_per_kg','industry_use_case']]
    out.to_csv(out_path, index=False)
    return out

def clean_products(raw_path, out_path, reference_clean_path=None):
    df = pd.read_csv(raw_path, dtype=str)
    col_map = map_product_cols(df.columns)
    df = df.rename(columns=col_map)

    expected = ['product_id','product_name','category','product_weight','fragility_index','shipping_type','is_active']
    for c in expected:
        if c not in df.columns:
            df[c] = np.nan

    df['product_name'] = df['product_name'].astype(str).str.strip()
    df['category'] = df['category'].astype(str).str.strip().str.lower().replace('nan', np.nan)
    df['shipping_type'] = df['shipping_type'].astype(str).str.strip().str.lower().replace('nan', np.nan)
    df['shipping_type'] = df['shipping_type'].replace({'air':'air','air ':'air',' air':'air','road ':'road',' road':'road','sea ':'sea',' sea':'sea','AIR':'air'})

    # Parse numerics
    df['product_weight'] = df['product_weight'].apply(parse_numeric_val)
    df['fragility_index'] = pd.to_numeric(df['fragility_index'], errors='coerce')

    # parse boolean
    df['is_active'] = df['is_active'].apply(parse_boolean)

    # Drop exact duplicates
    df = df.drop_duplicates()
    df = df[~df['product_name'].isna()]

    # Impute product_weight: use reference medians per category if available
    if reference_clean_path and Path(reference_clean_path).exists():
        ref = pd.read_csv(reference_clean_path)
        global_median = float(ref['product_weight'].median())
    else:
        global_median = float(df['product_weight'].median()) if df['product_weight'].notna().sum()>0 else 0.0

    df['product_weight'] = df['product_weight'].fillna(global_median)

    # fragility impute with mode or default 5
    if df['fragility_index'].notna().sum() > 0:
        modes = df['fragility_index'].mode()
        if len(modes) > 0:
            mode_val = int(modes.iloc[0])
        else:
            mode_val = 5
    else:
        mode_val = 5
    df['fragility_index'] = df['fragility_index'].fillna(mode_val).astype(int)

    # Ensure types and reorder
    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce').astype('Int64')
    df['product_weight'] = df['product_weight'].astype(float)

    out = df[['product_id','product_name','category','product_weight','fragility_index','shipping_type']]
    out.to_csv(out_path, index=False)
    return out

def run_all(reference_material_clean=None, reference_product_clean=None):
    mat_in = RAW / 'material_dataset_raw.csv'
    prod_in = RAW / 'product_dataset_raw.csv'
    mat_out = PROCESSED / 'material_dataset.csv'
    prod_out = PROCESSED / 'product_dataset.csv'
    clean_materials(mat_in, mat_out, reference_material_clean)
    clean_products(prod_in, prod_out, reference_product_clean)
    return {'material_out': str(mat_out), 'product_out': str(prod_out)}

if __name__ == '__main__':
    print('Running cleaning...')
    stats = run_all(reference_material_clean=None, reference_product_clean=None)
    print('Done. Wrote:', stats)
