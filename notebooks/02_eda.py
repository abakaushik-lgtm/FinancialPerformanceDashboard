"""
02_eda.py
Financial Performance Dashboard - Exploratory Data Analysis (EDA)
Author: Senior Data Analyst & BI Developer
Description: Performs multi-dimensional exploratory analysis using Pandas & Plotly, 
             generating statistical summaries and interactive charts for executive review.
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as gg

def load_data(filepath='data/cleaned_financial_data.csv'):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Cleaned dataset not found at {filepath}. Please run 01_data_cleaning.py first.")
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def perform_eda():
    df = load_data()
    print("=" * 60)
    print(" FINANCIAL PERFORMANCE DASHBOARD - EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    print(f"Total Transactions Analyzed: {len(df):,}")
    print(f"Date Range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    
    # 1. Overall Key Performance Indicators (KPIs)
    total_revenue = df['Revenue'].sum()
    total_cogs = df['Cost of Goods Sold (COGS)'].sum()
    total_opex = df['Operating Expense'].sum()
    total_marketing = df['Marketing Expense'].sum()
    total_tax = df['Tax'].sum()
    total_expenses = total_cogs + total_opex + total_marketing + total_tax
    gross_profit = df['Gross Profit'].sum()
    net_profit = df['Profit'].sum()
    net_margin = (net_profit / total_revenue) * 100
    gross_margin = (gross_profit / total_revenue) * 100
    total_budget = df['Budget'].sum()
    budget_var = total_revenue - total_budget
    budget_util = (total_revenue / total_budget) * 100
    
    print("\n--- [1] EXECUTIVE SUMMARY METRICS ---")
    print(f"Total Revenue:         ${total_revenue:,.2f}")
    print(f"Total Gross Profit:    ${gross_profit:,.2f} (Gross Margin: {gross_margin:.2f}%)")
    print(f"Total Expenses:        ${total_expenses:,.2f}")
    print(f"Total Net Profit:      ${net_profit:,.2f} (Net Margin: {net_margin:.2f}%)")
    print(f"Total Budget Target:   ${total_budget:,.2f}")
    print(f"Budget Variance:       ${budget_var:,.2f} (Utilization: {budget_util:.2f}%)")
    print(f"Average Order Value:   ${df['Revenue'].mean():,.2f}")

    # 2. Monthly Revenue & Profit Trend
    monthly_trend = df.groupby(df['Date'].dt.to_period('M')).agg({
        'Revenue': 'sum',
        'Profit': 'sum',
        'Budget': 'sum'
    }).reset_index()
    monthly_trend['DateStr'] = monthly_trend['Date'].astype(str)
    
    print("\n--- [2] MONTHLY TREND HIGHLIGHTS ---")
    best_rev_month = monthly_trend.loc[monthly_trend['Revenue'].idxmax()]
    worst_rev_month = monthly_trend.loc[monthly_trend['Revenue'].idxmin()]
    print(f"Peak Revenue Month:    {best_rev_month['DateStr']} (${best_rev_month['Revenue']:,.2f})")
    print(f"Lowest Revenue Month:  {worst_rev_month['DateStr']} (${worst_rev_month['Revenue']:,.2f})")

    # 3. Regional Breakdown
    regional_summary = df.groupby('Region').agg({
        'Revenue': 'sum',
        'Profit': 'sum',
        'Budget': 'sum'
    }).reset_index()
    regional_summary['Profit Margin %'] = (regional_summary['Profit'] / regional_summary['Revenue']) * 100
    regional_summary = regional_summary.sort_values(by='Revenue', ascending=False)
    
    print("\n--- [3] REGIONAL PERFORMANCE ---")
    for _, row in regional_summary.iterrows():
        print(f"Region: {row['Region']:<20} | Rev: ${row['Revenue']:>14,.2f} | Profit: ${row['Profit']:>12,.2f} | Margin: {row['Profit Margin %']:>5.2f}%")

    # 4. Product Category Performance
    cat_summary = df.groupby('Product Category').agg({
        'Revenue': 'sum',
        'Profit': 'sum',
        'Cost of Goods Sold (COGS)': 'sum'
    }).reset_index()
    cat_summary['Profit Margin %'] = (cat_summary['Profit'] / cat_summary['Revenue']) * 100
    cat_summary = cat_summary.sort_values(by='Revenue', ascending=False)
    
    print("\n--- [4] PRODUCT CATEGORY BREAKDOWN ---")
    for _, row in cat_summary.iterrows():
        print(f"Category: {row['Product Category']:<24} | Rev: ${row['Revenue']:>14,.2f} | Profit: ${row['Profit']:>12,.2f} | Margin: {row['Profit Margin %']:>5.2f}%")

    # 5. Top 10 Products by Revenue
    top_products = df.groupby('Product Name').agg({
        'Revenue': 'sum',
        'Profit': 'sum',
        'Transaction ID': 'count'
    }).rename(columns={'Transaction ID': 'Transactions'}).reset_index()
    top_products = top_products.sort_values(by='Revenue', ascending=False).head(10)
    
    print("\n--- [5] TOP 10 PRODUCTS BY REVENUE ---")
    for idx, row in top_products.reset_index(drop=True).iterrows():
        print(f"{idx+1:2d}. {row['Product Name']:<30} | Rev: ${row['Revenue']:>12,.2f} | Profit: ${row['Profit']:>10,.2f} | Orders: {row['Transactions']}")

    # 6. Year-over-Year Growth
    yoy_summary = df.groupby('Year').agg({
        'Revenue': 'sum',
        'Profit': 'sum',
        'Budget': 'sum'
    }).reset_index()
    yoy_summary['Rev YoY Growth %'] = yoy_summary['Revenue'].pct_change() * 100
    yoy_summary['Profit YoY Growth %'] = yoy_summary['Profit'].pct_change() * 100
    
    print("\n--- [6] YEAR-OVER-YEAR (YoY) PERFORMANCE ---")
    for _, row in yoy_summary.iterrows():
        growth_str = f"{row['Rev YoY Growth %']:.2f}%" if not np.isnan(row['Rev YoY Growth %']) else "N/A"
        print(f"Year {int(row['Year'])} | Revenue: ${row['Revenue']:>14,.2f} (YoY: {growth_str:>7}) | Profit: ${row['Profit']:>12,.2f}")

    print("\nEDA completed successfully.")

if __name__ == '__main__':
    perform_eda()
