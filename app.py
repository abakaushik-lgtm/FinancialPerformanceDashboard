"""
app.py
Financial Performance Dashboard & Business Insights - Streamlit Application
Author: Senior Data Analyst & BI Developer
Description: Modern, production-ready interactive financial performance web application.
"""

import os
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from streamlit.kpi_engine import calculate_kpis, calculate_yoy_growth

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Financial Performance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS Styles
css_path = os.path.join(os.path.dirname(__file__), 'streamlit', 'styles.css')
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Custom Plotly Template for Dark Theme
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_PRIMARY = "#6366f1"   # Indigo
COLOR_SUCCESS = "#10b981"   # Emerald Green
COLOR_WARNING = "#f59e0b"   # Amber
COLOR_DANGER = "#ef4444"    # Red
COLOR_INFO = "#3b82f6"      # Blue

# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_financial_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'cleaned_financial_data.csv')
    if not os.path.exists(csv_path):
        import importlib
        cleaning_mod = importlib.import_module('notebooks.01_data_cleaning')
        cleaning_mod.main()
        
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df_raw = load_financial_data()

# -----------------------------------------------------------------------------
# 3. SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/isometric-headers/100/line-chart.png", width=64)
st.sidebar.title("Financial Filters")
st.sidebar.markdown("Filter options dynamically update all metrics and charts.")

# Year Filter
years = sorted(df_raw['Year'].unique().tolist())
selected_years = st.sidebar.multiselect("Select Year(s)", options=years, default=years)

# Quarter Filter
quarters = sorted(df_raw['Quarter'].unique().tolist())
selected_quarters = st.sidebar.multiselect("Select Quarter(s)", options=quarters, default=quarters)

# Region Filter
regions = sorted(df_raw['Region'].unique().tolist())
selected_regions = st.sidebar.multiselect("Select Region(s)", options=regions, default=regions)

# Product Category Filter
categories = sorted(df_raw['Product Category'].unique().tolist())
selected_categories = st.sidebar.multiselect("Select Product Category", options=categories, default=categories)

# Business Unit Filter
business_units = sorted(df_raw['Business Unit'].unique().tolist())
selected_bus = st.sidebar.multiselect("Select Business Unit", options=business_units, default=business_units)

# Department Filter
departments = sorted(df_raw['Department'].unique().tolist())
selected_depts = st.sidebar.multiselect("Select Department", options=departments, default=departments)

# Apply Filter Mask
mask = (
    df_raw['Year'].isin(selected_years) &
    df_raw['Quarter'].isin(selected_quarters) &
    df_raw['Region'].isin(selected_regions) &
    df_raw['Product Category'].isin(selected_categories) &
    df_raw['Business Unit'].isin(selected_bus) &
    df_raw['Department'].isin(selected_depts)
)

df_filtered = df_raw[mask].copy()

# Reset Button
if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset Info:**")
st.sidebar.info(f"Filtered Records: **{len(df_filtered):,}** / {len(df_raw):,}")

# -----------------------------------------------------------------------------
# 4. MAIN HEADER & EXECUTIVE KPIS
# -----------------------------------------------------------------------------
st.title("💼 Financial Performance & Business Insights Dashboard")
st.markdown("Comprehensive executive dashboard analyzing financial metrics, profitability, variance, and forecast scenarios.")

kpis = calculate_kpis(df_filtered)
yoy = calculate_yoy_growth(df_filtered)

# KPI Cards Layout (6 Columns)
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        label="Total Revenue",
        value=f"${kpis['total_revenue']/1e6:.2f}M",
        delta=f"{yoy['rev_growth']:+.1f}% YoY" if yoy['rev_growth'] != 0 else None
    )

with col2:
    st.metric(
        label="Gross Profit",
        value=f"${kpis['total_gross_profit']/1e6:.2f}M",
        delta=f"{kpis['gross_margin']:.1f}% Margin"
    )

with col3:
    st.metric(
        label="Total Expenses",
        value=f"${kpis['total_expenses']/1e6:.2f}M",
        delta=f"{kpis['cost_ratio']:.1f}% Cost Ratio",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="Net Profit",
        value=f"${kpis['total_net_profit']/1e6:.2f}M",
        delta=f"{kpis['net_margin']:.1f}% Net Margin"
    )

with col5:
    util = kpis['budget_utilization']
    st.metric(
        label="Budget Target",
        value=f"${kpis['total_budget']/1e6:.2f}M",
        delta=f"{util:.1f}% Utilized"
    )

with col6:
    st.metric(
        label="Average Order Value",
        value=f"${kpis['aov']:,.0f}",
        delta=f"{kpis['total_orders']:,} Txns"
    )

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. DASHBOARD TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Executive Summary",
    "🌍 Regional Performance",
    "📦 Product & Customer Analytics",
    "💸 Expense Analysis",
    "📈 Financial Forecast & Scenario",
    "🔍 Data Inspector & Export"
])

# =============================================================================
# TAB 1: EXECUTIVE SUMMARY
# =============================================================================
with tab1:
    st.subheader("Executive Financial Performance & Monthly Trends")
    
    if df_filtered.empty:
        st.warning("No data available for selected filters.")
    else:
        # Monthly Revenue & Profit Trend vs Budget
        df_monthly = df_filtered.groupby(df_filtered['Date'].dt.to_period('M')).agg({
            'Revenue': 'sum',
            'Profit': 'sum',
            'Budget': 'sum'
        }).reset_index()
        df_monthly['Month_Str'] = df_monthly['Date'].astype(str)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=df_monthly['Month_Str'], y=df_monthly['Revenue'],
            name='Revenue', marker_color=COLOR_PRIMARY, opacity=0.8
        ))
        fig_trend.add_trace(go.Bar(
            x=df_monthly['Month_Str'], y=df_monthly['Profit'],
            name='Net Profit', marker_color=COLOR_SUCCESS, opacity=0.9
        ))
        fig_trend.add_trace(go.Scatter(
            x=df_monthly['Month_Str'], y=df_monthly['Budget'],
            name='Budget Target', mode='lines+markers',
            line=dict(color=COLOR_WARNING, width=3, dash='dash')
        ))
        fig_trend.update_layout(
            title="Monthly Revenue & Net Profit Trend vs. Budget Target ($)",
            xaxis_title="Month", yaxis_title="Amount ($)",
            barmode='group', template=PLOTLY_TEMPLATE, height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Row 2: Business Unit Performance & Budget Variance
        c1, c2 = st.columns(2)
        
        with c1:
            bu_summary = df_filtered.groupby('Business Unit').agg({'Revenue': 'sum', 'Profit': 'sum'}).reset_index()
            fig_bu = px.bar(
                bu_summary, x='Business Unit', y=['Revenue', 'Profit'],
                barmode='group', title="Revenue & Net Profit by Business Unit ($)",
                color_discrete_sequence=[COLOR_PRIMARY, COLOR_SUCCESS],
                template=PLOTLY_TEMPLATE, height=380
            )
            st.plotly_chart(fig_bu, use_container_width=True)
            
        with c2:
            bu_budget = df_filtered.groupby('Business Unit').agg({'Actual Sales': 'sum', 'Budget': 'sum'}).reset_index()
            bu_budget['Variance'] = bu_budget['Actual Sales'] - bu_budget['Budget']
            bu_budget['Color'] = np.where(bu_budget['Variance'] >= 0, COLOR_SUCCESS, COLOR_DANGER)
            
            fig_var = px.bar(
                bu_budget, x='Business Unit', y='Variance',
                color='Color', color_discrete_map='identity',
                title="Budget Variance by Business Unit ($ Over / Under Target)",
                template=PLOTLY_TEMPLATE, height=380
            )
            st.plotly_chart(fig_var, use_container_width=True)

# =============================================================================
# TAB 2: REGIONAL PERFORMANCE
# =============================================================================
with tab2:
    st.subheader("Geographic & Regional Performance Matrix")
    
    if df_filtered.empty:
        st.warning("No data available.")
    else:
        r1, r2 = st.columns([1.2, 1.0])
        
        with r1:
            reg_df = df_filtered.groupby('Region').agg({'Revenue': 'sum', 'Profit': 'sum'}).reset_index()
            reg_df['Profit Margin %'] = (reg_df['Profit'] / reg_df['Revenue']) * 100
            
            fig_reg = px.bar(
                reg_df, x='Region', y='Revenue', color='Profit Margin %',
                color_continuous_scale='Viridis',
                title="Regional Revenue ($) colored by Profit Margin %",
                template=PLOTLY_TEMPLATE, height=400
            )
            st.plotly_chart(fig_reg, use_container_width=True)
            
        with r2:
            city_df = df_filtered.groupby(['City', 'Country', 'Region']).agg({'Revenue': 'sum', 'Profit': 'sum'}).reset_index()
            top_cities = city_df.sort_values(by='Revenue', ascending=False).head(10)
            
            fig_city = px.bar(
                top_cities, y='City', x='Revenue', color='Region',
                orientation='h', title="Top 10 Cities by Revenue ($)",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template=PLOTLY_TEMPLATE, height=400
            )
            fig_city.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_city, use_container_width=True)
            
        st.markdown("### Country-Level Financial Detailed Summary")
        country_summary = df_filtered.groupby(['Region', 'Country']).agg({
            'Revenue': 'sum',
            'Gross Profit': 'sum',
            'Profit': 'sum',
            'Budget': 'sum',
            'Transaction ID': 'count'
        }).rename(columns={'Transaction ID': 'Transactions'}).reset_index()
        country_summary['Net Margin %'] = (country_summary['Profit'] / country_summary['Revenue']) * 100
        country_summary['Budget Util %'] = (country_summary['Revenue'] / country_summary['Budget']) * 100
        
        st.dataframe(
            country_summary.style.format({
                'Revenue': '${:,.2f}', 'Gross Profit': '${:,.2f}',
                'Profit': '${:,.2f}', 'Budget': '${:,.2f}',
                'Net Margin %': '{:.2f}%', 'Budget Util %': '{:.2f}%'
            }),
            use_container_width=True
        )

# =============================================================================
# TAB 3: PRODUCT & CUSTOMER ANALYTICS
# =============================================================================
with tab3:
    st.subheader("Product Portfolio & Customer Segment Performance")
    
    if df_filtered.empty:
        st.warning("No data available.")
    else:
        p1, p2 = st.columns(2)
        
        with p1:
            cat_df = df_filtered.groupby('Product Category').agg({'Revenue': 'sum', 'Profit': 'sum'}).reset_index()
            fig_tree = px.treemap(
                cat_df, path=['Product Category'], values='Revenue', color='Profit',
                color_continuous_scale='RdYlGn',
                title="Revenue Contribution by Product Category (Colored by Net Profit)",
                template=PLOTLY_TEMPLATE, height=420
            )
            st.plotly_chart(fig_tree, use_container_width=True)
            
        with p2:
            prod_df = df_filtered.groupby('Product Name').agg({'Revenue': 'sum', 'Profit': 'sum'}).reset_index()
            top_10_prod = prod_df.sort_values(by='Revenue', ascending=False).head(10)
            
            fig_top = px.bar(
                top_10_prod, x='Revenue', y='Product Name', orientation='h',
                title="Top 10 Products by Revenue ($)",
                color='Profit', color_continuous_scale='Blues',
                template=PLOTLY_TEMPLATE, height=420
            )
            fig_top.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_top, use_container_width=True)
            
        st.markdown("---")
        c_sub1, c_sub2 = st.columns(2)
        
        with c_sub1:
            prod_margin = df_filtered.groupby(['Product Name', 'Product Category']).agg({'Revenue': 'sum', 'Profit': 'sum'}).reset_index()
            prod_margin['Margin %'] = (prod_margin['Profit'] / prod_margin['Revenue']) * 100
            
            fig_scatter = px.scatter(
                prod_margin, x='Revenue', y='Margin %', color='Product Category',
                size='Profit', hover_data=['Product Name'],
                title="Product Revenue vs. Profit Margin % Scatter Plot",
                template=PLOTLY_TEMPLATE, height=400
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with c_sub2:
            seg_channel = df_filtered.groupby(['Customer Segment', 'Sales Channel']).agg({'Revenue': 'sum'}).reset_index()
            fig_seg = px.bar(
                seg_channel, x='Customer Segment', y='Revenue', color='Sales Channel',
                barmode='stack', title="Revenue by Customer Segment & Sales Channel ($)",
                template=PLOTLY_TEMPLATE, height=400
            )
            st.plotly_chart(fig_seg, use_container_width=True)

# =============================================================================
# TAB 4: EXPENSE ANALYSIS
# =============================================================================
with tab4:
    st.subheader("Expense Structure & Departmental Cost Breakdown")
    
    if df_filtered.empty:
        st.warning("No data available.")
    else:
        e1, e2 = st.columns(2)
        
        with e1:
            # Waterfall Chart for P&L Breakdown
            rev = df_filtered['Revenue'].sum()
            cogs = df_filtered['Cost of Goods Sold (COGS)'].sum()
            opex = df_filtered['Operating Expense'].sum()
            mkt = df_filtered['Marketing Expense'].sum()
            tax = df_filtered['Tax'].sum()
            profit = df_filtered['Profit'].sum()
            
            fig_waterfall = go.Figure(go.Waterfall(
                name = "P&L Statement", orientation = "v",
                measure = ["relative", "relative", "relative", "relative", "relative", "total"],
                x = ["Revenue", "COGS", "OpEx", "Marketing", "Tax", "Net Profit"],
                textposition = "outside",
                text = [f"${v/1e6:.1f}M" for v in [rev, -cogs, -opex, -mkt, -tax, profit]],
                y = [rev, -cogs, -opex, -mkt, -tax, profit],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
                decreasing = {"marker":{"color":COLOR_DANGER}},
                increasing = {"marker":{"color":COLOR_SUCCESS}},
                totals = {"marker":{"color":COLOR_PRIMARY}}
            ))
            fig_waterfall.update_layout(
                title="P&L Financial Waterfall Breakdown ($)",
                template=PLOTLY_TEMPLATE, height=420
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
        with e2:
            # Department Operating & Marketing Expense Breakdown
            dept_exp = df_filtered.groupby('Department').agg({
                'Operating Expense': 'sum',
                'Marketing Expense': 'sum'
            }).reset_index()
            
            fig_dept = px.bar(
                dept_exp, x='Department', y=['Operating Expense', 'Marketing Expense'],
                title="Departmental Operating & Marketing Expenses ($)",
                barmode='group', color_discrete_sequence=[COLOR_WARNING, COLOR_INFO],
                template=PLOTLY_TEMPLATE, height=420
            )
            st.plotly_chart(fig_dept, use_container_width=True)

# =============================================================================
# TAB 5: FINANCIAL FORECAST & WHAT-IF SCENARIO SIMULATOR
# =============================================================================
with tab5:
    st.subheader("🔮 What-If Scenario Planning & Revenue Simulator")
    st.markdown("Adjust key business drivers below to model real-time impacts on Revenue, Costs, and Net Profit.")
    
    if df_filtered.empty:
        st.warning("No data available for scenario modeling.")
    else:
        # Scenario Sliders
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            price_change = st.slider("Price Change (%)", min_value=-20.0, max_value=30.0, value=0.0, step=1.0)
        with s_col2:
            cogs_change = st.slider("COGS Shift (%)", min_value=-20.0, max_value=20.0, value=0.0, step=1.0)
        with s_col3:
            mkt_boost = st.slider("Marketing Spend Change (%)", min_value=-30.0, max_value=50.0, value=0.0, step=5.0)
            
        base_rev = df_filtered['Revenue'].sum()
        base_cogs = df_filtered['Cost of Goods Sold (COGS)'].sum()
        base_opex = df_filtered['Operating Expense'].sum()
        base_mkt = df_filtered['Marketing Expense'].sum()
        base_tax = df_filtered['Tax'].sum()
        base_profit = df_filtered['Profit'].sum()
        
        # Calculate Simulated Financials
        sim_rev = base_rev * (1 + price_change / 100.0) + (base_mkt * (mkt_boost / 100.0) * 1.5) # Marketing elasticity assumption
        sim_cogs = base_cogs * (1 + cogs_change / 100.0)
        sim_mkt = base_mkt * (1 + mkt_boost / 100.0)
        sim_opex = base_opex
        sim_tax = (sim_rev - sim_cogs - sim_opex - sim_mkt) * 0.15
        if sim_tax < 0: sim_tax = 0.0
        
        sim_profit = sim_rev - sim_cogs - sim_opex - sim_mkt - sim_tax
        sim_margin = (sim_profit / sim_rev * 100) if sim_rev > 0 else 0.0
        
        rev_delta = sim_rev - base_rev
        profit_delta = sim_profit - base_profit
        
        st.markdown("### Simulated Scenario Results vs. Baseline")
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Simulated Revenue", f"${sim_rev/1e6:.2f}M", delta=f"${rev_delta/1e6:+.2f}M")
        sc2.metric("Simulated Net Profit", f"${sim_profit/1e6:.2f}M", delta=f"${profit_delta/1e6:+.2f}M")
        sc3.metric("Simulated Net Margin", f"{sim_margin:.2f}%", delta=f"{sim_margin - (base_profit/base_rev*100):+.2f}%")
        sc4.metric("Marketing ROI Impact", f"{(sim_rev - base_rev)/(sim_mkt - base_mkt):.2f}x" if (sim_mkt - base_mkt) != 0 else "N/A")
        
        # Monthly Projection Chart
        df_m = df_filtered.groupby(df_filtered['Date'].dt.to_period('M'))['Revenue'].sum().reset_index()
        df_m['Month_Str'] = df_m['Date'].astype(str)
        df_m['Simulated_Revenue'] = df_m['Revenue'] * (1 + price_change / 100.0)
        
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Scatter(x=df_m['Month_Str'], y=df_m['Revenue'], name='Baseline Revenue', line=dict(color=COLOR_PRIMARY, width=3)))
        fig_sim.add_trace(go.Scatter(x=df_m['Month_Str'], y=df_m['Simulated_Revenue'], name='Simulated Scenario Revenue', line=dict(color=COLOR_SUCCESS, width=3, dash='dash')))
        fig_sim.update_layout(title="Monthly Revenue Trend: Baseline vs. Simulated Scenario ($)", template=PLOTLY_TEMPLATE, height=400)
        st.plotly_chart(fig_sim, use_container_width=True)

# =============================================================================
# TAB 6: DATA INSPECTOR & EXPORT
# =============================================================================
with tab6:
    st.subheader("Data Inspector & CSV Export")
    
    # Search box
    search_term = st.text_input("🔍 Search Transactions (Product, Region, City, Channel, etc.):", "")
    
    if search_term:
        mask_search = df_filtered.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)
        df_display = df_filtered[mask_search]
    else:
        df_display = df_filtered
        
    st.markdown(f"Displaying **{len(df_display):,}** matching rows.")
    st.dataframe(df_display.head(500), use_container_width=True)
    
    # Download Button
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name="filtered_financial_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Financial Performance Dashboard | Developed by Senior Data Analyst & BI Developer | Powered by Python & Streamlit</p>", unsafe_allow_html=True)
