"""
kpi_engine.py
Financial KPI Calculation Engine
Author: Senior Data Analyst & BI Developer
Description: Computes financial KPIs, margins, ratios, and YoY comparative metrics for Streamlit UI.
"""

import numpy as np
import pandas as pd

def calculate_kpis(df):
    """Compute overall financial performance KPIs from filtered dataframe."""
    if df.empty:
        return {
            'total_revenue': 0.0, 'total_gross_profit': 0.0, 'total_expenses': 0.0,
            'total_net_profit': 0.0, 'gross_margin': 0.0, 'net_margin': 0.0,
            'total_budget': 0.0, 'budget_variance': 0.0, 'budget_utilization': 0.0,
            'aov': 0.0, 'cost_ratio': 0.0, 'total_orders': 0
        }
        
    revenue = df['Revenue'].sum()
    cogs = df['Cost of Goods Sold (COGS)'].sum()
    opex = df['Operating Expense'].sum()
    marketing = df['Marketing Expense'].sum()
    tax = df['Tax'].sum()
    
    gross_profit = df['Gross Profit'].sum() if 'Gross Profit' in df.columns else (revenue - cogs)
    net_profit = df['Profit'].sum()
    expenses = cogs + opex + marketing + tax
    
    gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0.0
    net_margin = (net_profit / revenue * 100) if revenue > 0 else 0.0
    
    budget = df['Budget'].sum()
    budget_variance = revenue - budget
    budget_utilization = (revenue / budget * 100) if budget > 0 else 0.0
    
    aov = df['Revenue'].mean()
    cost_ratio = (expenses / revenue * 100) if revenue > 0 else 0.0
    total_orders = len(df)
    
    return {
        'total_revenue': revenue,
        'total_cogs': cogs,
        'total_opex': opex,
        'total_marketing': marketing,
        'total_tax': tax,
        'total_gross_profit': gross_profit,
        'total_expenses': expenses,
        'total_net_profit': net_profit,
        'gross_margin': gross_margin,
        'net_margin': net_margin,
        'total_budget': budget,
        'budget_variance': budget_variance,
        'budget_utilization': budget_utilization,
        'aov': aov,
        'cost_ratio': cost_ratio,
        'total_orders': total_orders
    }

def calculate_yoy_growth(df):
    """Compute YoY revenue and profit growth percentages."""
    if df.empty:
        return {'rev_growth': 0.0, 'profit_growth': 0.0}
        
    yearly = df.groupby('Year').agg({'Revenue': 'sum', 'Profit': 'sum'}).reset_index()
    if len(yearly) < 2:
        return {'rev_growth': 0.0, 'profit_growth': 0.0}
        
    latest_year = yearly.iloc[-1]
    prev_year = yearly.iloc[-2]
    
    rev_growth = ((latest_year['Revenue'] - prev_year['Revenue']) / prev_year['Revenue'] * 100) if prev_year['Revenue'] > 0 else 0.0
    profit_growth = ((latest_year['Profit'] - prev_year['Profit']) / prev_year['Profit'] * 100) if prev_year['Profit'] > 0 else 0.0
    
    return {'rev_growth': rev_growth, 'profit_growth': profit_growth}
