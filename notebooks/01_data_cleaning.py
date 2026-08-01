"""
01_Data_Cleaning.py
Financial Performance Dashboard - Data Generation & Cleaning Pipeline
Author: Senior Data Analyst & BI Developer
Description: Generates 12,000+ realistic raw financial transactions with deliberate anomalies, 
             performs rigorous data cleaning (missing value imputation, deduplication, 
             IQR outlier capping, dtype conversion, and metric feature engineering), 
             and exports raw and cleaned CSV datasets.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def create_directories():
    """Ensure output directories exist."""
    directories = ['data', 'sql', 'notebooks', 'powerbi', 'streamlit', 'dashboard_images', 'reports']
    for d in directories:
        os.makedirs(d, exist_ok=True)
    print("Directories verified.")

def generate_raw_financial_data(num_records=12000, seed=42):
    """Generate realistic raw financial dataset with synthetic anomalies."""
    np.random.seed(seed)
    
    # Dates spanning 2023 to 2025
    start_date = datetime(2023, 1, 1)
    date_list = [start_date + timedelta(days=int(i)) for i in np.random.randint(0, 1095, size=num_records)]
    date_list.sort()
    
    # Structural mappings
    region_country_city = {
        'North America': [('USA', 'New York'), ('USA', 'San Francisco'), ('USA', 'Chicago'), ('Canada', 'Toronto')],
        'Europe': [('UK', 'London'), ('Germany', 'Frankfurt'), ('France', 'Paris'), ('Netherlands', 'Amsterdam')],
        'Asia Pacific': [('Japan', 'Tokyo'), ('Australia', 'Sydney'), ('Singapore', 'Singapore'), ('India', 'Mumbai')],
        'Latin America': [('Brazil', 'Sao Paulo'), ('Mexico', 'Mexico City'), ('Colombia', 'Bogota')],
        'Middle East & Africa': [('UAE', 'Dubai'), ('Saudi Arabia', 'Riyadh'), ('South Africa', 'Johannesburg')]
    }
    
    business_units = ['Enterprise Solutions', 'Consumer Goods', 'Digital Services', 'Financial Services']
    departments = ['Sales', 'Marketing', 'Engineering', 'Operations', 'Customer Support']
    
    categories_products = {
        'Electronics': ['Smart Hub Pro', 'UltraBook Enterprise', '4K Display Monitor', 'Wireless Headset Pro'],
        'Software Services': ['SaaS ERP License', 'AI Analytics Platform', 'CyberShield Security', 'Cloud Database Engine'],
        'Hardware Systems': ['Server Rack X1', 'Network Switch 48P', 'Storage Array V2', 'Edge Compute Node'],
        'Cloud Infrastructure': ['Dedicated Cloud Compute', 'Object Storage Multi-Region', 'Load Balancer Cluster'],
        'Professional Consulting': ['Advisory Subscription', 'Implementation Services', '24/7 Premium Support']
    }
    
    customer_segments = ['Enterprise', 'Mid-Market', 'SMB', 'Consumer']
    sales_channels = ['Direct Sales', 'Online Store', 'Partner Channel', 'Reseller Network']
    
    records = []
    
    for i in range(num_records):
        txn_id = f"TXN-{10001 + i}"
        dt = date_list[i]
        
        # Region selection & hierarchy
        region = np.random.choice(list(region_country_city.keys()), p=[0.35, 0.25, 0.20, 0.10, 0.10])
        country, city = region_country_city[region][np.random.randint(0, len(region_country_city[region]))]
        
        bu = np.random.choice(business_units)
        dept = np.random.choice(departments)
        
        category = np.random.choice(list(categories_products.keys()), p=[0.25, 0.30, 0.15, 0.20, 0.10])
        product = np.random.choice(categories_products[category])
        
        segment = np.random.choice(customer_segments, p=[0.40, 0.30, 0.20, 0.10])
        channel = np.random.choice(sales_channels, p=[0.35, 0.30, 0.20, 0.15])
        
        # Base financial dynamics by category
        if category == 'Software Services':
            base_rev = np.random.uniform(5000, 45000)
            cogs_pct = np.random.uniform(0.15, 0.30)
        elif category == 'Cloud Infrastructure':
            base_rev = np.random.uniform(8000, 60000)
            cogs_pct = np.random.uniform(0.30, 0.45)
        elif category == 'Electronics':
            base_rev = np.random.uniform(1200, 15000)
            cogs_pct = np.random.uniform(0.55, 0.72)
        elif category == 'Hardware Systems':
            base_rev = np.random.uniform(10000, 85000)
            cogs_pct = np.random.uniform(0.50, 0.68)
        else: # Professional Consulting
            base_rev = np.random.uniform(3000, 35000)
            cogs_pct = np.random.uniform(0.40, 0.55)
            
        # Add YoY growth trend (2023 -> 2024 -> 2025)
        year = dt.year
        growth_factor = 1.0 if year == 2023 else (1.12 if year == 2024 else 1.25)
        # Seasonality boost in Q4
        month = dt.month
        seasonality = 1.25 if month in [11, 12] else (1.10 if month in [9, 10] else 1.0)
        
        revenue = round(base_rev * growth_factor * seasonality, 2)
        cogs = round(revenue * cogs_pct, 2)
        operating_expense = round(revenue * np.random.uniform(0.10, 0.22), 2)
        marketing_expense = round(revenue * np.random.uniform(0.04, 0.12), 2)
        discount = round(revenue * np.random.uniform(0.0, 0.15), 2)
        tax = round((revenue - cogs - operating_expense) * np.random.uniform(0.08, 0.18), 2)
        if tax < 0:
            tax = 0.0
            
        profit = round(revenue - cogs - operating_expense - marketing_expense - tax, 2)
        profit_margin = round((profit / revenue) * 100, 2) if revenue > 0 else 0.0
        
        budget = round(revenue * np.random.uniform(0.88, 1.12), 2)
        actual_sales = revenue
        
        records.append({
            'Transaction ID': txn_id,
            'Date': dt.strftime('%Y-%m-%d'),
            'Month': dt.strftime('%B'),
            'Quarter': f"Q{(dt.month-1)//3 + 1}",
            'Year': year,
            'Region': region,
            'Country': country,
            'City': city,
            'Business Unit': bu,
            'Department': dept,
            'Product Category': category,
            'Product Name': product,
            'Customer Segment': segment,
            'Sales Channel': channel,
            'Revenue': revenue,
            'Cost of Goods Sold (COGS)': cogs,
            'Operating Expense': operating_expense,
            'Marketing Expense': marketing_expense,
            'Discount': discount,
            'Tax': tax,
            'Profit': profit,
            'Profit Margin': profit_margin,
            'Budget': budget,
            'Actual Sales': actual_sales
        })
        
    df = pd.DataFrame(records)
    
    # Introduce deliberate real-world data quality anomalies for cleaning demonstration:
    # 1. Missing Values (~2.5% missing in Marketing Expense, Discount, Customer Segment)
    missing_idx_mkt = np.random.choice(df.index, size=int(0.025 * num_records), replace=False)
    df.loc[missing_idx_mkt, 'Marketing Expense'] = np.nan
    
    missing_idx_disc = np.random.choice(df.index, size=int(0.02 * num_records), replace=False)
    df.loc[missing_idx_disc, 'Discount'] = np.nan
    
    missing_idx_seg = np.random.choice(df.index, size=int(0.015 * num_records), replace=False)
    df.loc[missing_idx_seg, 'Customer Segment'] = np.nan
    
    # 2. Outliers / Extremes (~0.5% data entry errors)
    outlier_idx = np.random.choice(df.index, size=int(0.005 * num_records), replace=False)
    df.loc[outlier_idx, 'Revenue'] = df.loc[outlier_idx, 'Revenue'] * np.random.uniform(8.0, 15.0)
    
    # 3. Duplicate Rows (~1.5% duplicates)
    dup_idx = np.random.choice(df.index, size=int(0.015 * num_records), replace=False)
    duplicates = df.loc[dup_idx].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # 4. Text Inconsistencies (extra whitespace, lowercase)
    unstandard_idx = np.random.choice(df.index, size=int(0.03 * num_records), replace=False)
    df.loc[unstandard_idx, 'Region'] = df.loc[unstandard_idx, 'Region'].str.lower()
    
    unstandard_seg_idx = np.random.choice(df.index, size=int(0.02 * num_records), replace=False)
    df.loc[unstandard_seg_idx, 'Customer Segment'] = df.loc[unstandard_seg_idx, 'Customer Segment'].astype(str) + " "
    
    return df

def clean_financial_data(df):
    """Execute rigorous data cleaning pipeline on raw dataset."""
    print(f"\n--- Starting Data Cleaning Routine ---")
    print(f"Raw dataset shape: {df.shape}")
    
    # Step 1: Deduplication
    initial_count = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    df = df.drop_duplicates(subset=['Transaction ID']).reset_index(drop=True)
    dups_removed = initial_count - len(df)
    print(f"[1/6] Duplicate records removed: {dups_removed}")
    
    # Step 2: Text Standardization
    text_cols = ['Region', 'Country', 'City', 'Business Unit', 'Department', 
                 'Product Category', 'Product Name', 'Customer Segment', 'Sales Channel']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            # Restore specific acronyms
            df[col] = df[col].replace({'Smb': 'SMB', 'Uae': 'UAE', 'Usa': 'USA', 'Uk': 'UK', 'Ai': 'AI', 'Erp': 'ERP', 'Saas': 'SaaS'})
    print("[2/6] Text fields standardized and trimmed.")
    
    # Step 3: Handle Missing Values
    # Categorical missing values -> Mode or 'Unknown'
    if 'Customer Segment' in df.columns:
        df['Customer Segment'] = df['Customer Segment'].replace({'Nan': 'Enterprise', 'None': 'Enterprise'})
        df['Customer Segment'] = df['Customer Segment'].fillna('Enterprise')
        
    # Numerical missing values -> Group median or zero fill for optional metrics
    if 'Marketing Expense' in df.columns:
        df['Marketing Expense'] = df.groupby('Product Category')['Marketing Expense'].transform(lambda x: x.fillna(x.median()))
    if 'Discount' in df.columns:
        df['Discount'] = df['Discount'].fillna(0.0)
    print("[3/6] Missing values imputed.")
    
    # Step 4: Convert Data Types & Dates
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Quarter'] = 'Q' + df['Date'].dt.quarter.astype(str)
    
    numeric_cols = ['Revenue', 'Cost of Goods Sold (COGS)', 'Operating Expense', 
                    'Marketing Expense', 'Discount', 'Tax', 'Budget', 'Actual Sales']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    print("[4/6] Data types and date dimensions converted.")
    
    # Step 5: Detect & Treat Outliers using IQR Capping for Revenue & Expenses
    for col in ['Revenue', 'Operating Expense']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 3.0 * IQR # 3x IQR conservative upper limit
        outlier_count = (df[col] > upper_bound).sum()
        if outlier_count > 0:
            df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
            print(f"[5/6] Outliers treated in {col}: {outlier_count} records capped at {upper_bound:.2f}")
            
    # Step 6: Recalculate Financial Metrics for Absolute Accuracy
    df['Gross Profit'] = np.round(df['Revenue'] - df['Cost of Goods Sold (COGS)'], 2)
    df['Operating Profit'] = np.round(df['Gross Profit'] - df['Operating Expense'] - df['Marketing Expense'], 2)
    df['Profit'] = np.round(df['Operating Profit'] - df['Tax'], 2)
    df['Profit Margin'] = np.where(df['Revenue'] > 0, np.round((df['Profit'] / df['Revenue']) * 100, 2), 0.0)
    df['Gross Margin'] = np.where(df['Revenue'] > 0, np.round((df['Gross Profit'] / df['Revenue']) * 100, 2), 0.0)
    df['Budget Variance'] = np.round(df['Actual Sales'] - df['Budget'], 2)
    df['Budget Utilization'] = np.where(df['Budget'] > 0, np.round((df['Actual Sales'] / df['Budget']) * 100, 2), 100.0)
    df['Total Expense'] = np.round(df['Cost of Goods Sold (COGS)'] + df['Operating Expense'] + df['Marketing Expense'] + df['Tax'], 2)
    df['Cost Ratio'] = np.where(df['Revenue'] > 0, np.round((df['Total Expense'] / df['Revenue']) * 100, 2), 0.0)
    
    print("[6/6] Calculated financial columns engineered.")
    print(f"Cleaned dataset shape: {df.shape}")
    
    return df

def main():
    create_directories()
    raw_path = 'data/raw_financial_data.csv'
    cleaned_path = 'data/cleaned_financial_data.csv'
    
    print("Generating raw financial dataset...")
    df_raw = generate_raw_financial_data(num_records=12000, seed=42)
    df_raw.to_csv(raw_path, index=False)
    print(f"Raw financial dataset saved to '{raw_path}' ({len(df_raw)} rows).")
    
    df_cleaned = clean_financial_data(df_raw)
    df_cleaned.to_csv(cleaned_path, index=False)
    print(f"Cleaned dataset successfully exported to '{cleaned_path}' ({len(df_cleaned)} rows).")

if __name__ == '__main__':
    main()
