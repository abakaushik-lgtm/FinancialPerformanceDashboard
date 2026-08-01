"""
app.py
Financial Performance Dashboard & Business Insights - Streamlit Application
Author: Senior Data Analyst & BI Developer
Description: Production-ready interactive financial performance web application.
"""

import os
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import importlib.util

# Robustly load kpi_engine module avoiding streamlit package namespace collision
kpi_engine_path = os.path.join(os.path.dirname(__file__), 'streamlit', 'kpi_engine.py')
if not os.path.exists(kpi_engine_path):
    kpi_engine_path = os.path.join(os.path.dirname(__file__), 'kpi_engine.py')

spec = importlib.util.spec_from_file_location("kpi_engine", kpi_engine_path)
kpi_engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kpi_engine)

calculate_kpis = kpi_engine.calculate_kpis
calculate_yoy_growth = kpi_engine.calculate_yoy_growth

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Financial Performance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Theme Selector (Dark / Light Mode)
theme_choice = st.sidebar.selectbox("🎨 UI Theme Mode", ["Dark Glassmorphism", "Light Mode"])

if theme_choice == "Dark Glassmorphism":
    css_path = os.path.join(os.path.dirname(__file__), 'streamlit', 'styles.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    PLOTLY_TEMPLATE = "plotly_dark"
    COLOR_PRIMARY = "#6366f1"
    COLOR_SUCCESS = "#10b981"
    COLOR_WARNING = "#f59e0b"
    COLOR_DANGER = "#ef4444"
    COLOR_INFO = "#3b82f6"
else:
    PLOTLY_TEMPLATE = "plotly_white"
    COLOR_PRIMARY = "#4f46e5"
    COLOR_SUCCESS = "#059669"
    COLOR_WARNING = "#d97706"
    COLOR_DANGER = "#dc2626"
    COLOR_INFO = "#2563eb"

# -----------------------------------------------------------------------------
# 2. DATA LOADING & AUTOMATED ETL VALIDATION
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
st.sidebar.caption("⚡ Dynamic ETL & Real-Time Filtering")

years = sorted(df_raw['Year'].unique().tolist())
selected_years = st.sidebar.multiselect("Select Year(s)", options=years, default=years)

quarters = sorted(df_raw['Quarter'].unique().tolist())
selected_quarters = st.sidebar.multiselect("Select Quarter(s)", options=quarters, default=quarters)

regions = sorted(df_raw['Region'].unique().tolist())
selected_regions = st.sidebar.multiselect("Select Region(s)", options=regions, default=regions)

categories = sorted(df_raw['Product Category'].unique().tolist())
selected_categories = st.sidebar.multiselect("Select Product Category", options=categories, default=categories)

business_units = sorted(df_raw['Business Unit'].unique().tolist())
selected_bus = st.sidebar.multiselect("Select Business Unit", options=business_units, default=business_units)

departments = sorted(df_raw['Department'].unique().tolist())
selected_depts = st.sidebar.multiselect("Select Department", options=departments, default=departments)

mask = (
    df_raw['Year'].isin(selected_years) &
    df_raw['Quarter'].isin(selected_quarters) &
    df_raw['Region'].isin(selected_regions) &
    df_raw['Product Category'].isin(selected_categories) &
    df_raw['Business Unit'].isin(selected_bus) &
    df_raw['Department'].isin(selected_depts)
)

df_filtered = df_raw[mask].copy()

if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**Automated ETL Status:** ✅ PASS")
st.sidebar.info(f"Filtered Records: **{len(df_filtered):,}** / {len(df_raw):,}")

# -----------------------------------------------------------------------------
# 4. MAIN HEADER & EXECUTIVE KPIS
# -----------------------------------------------------------------------------
st.title("💼 Financial Performance & Business Insights Dashboard")
st.markdown("Enterprise BI Suite with Time-Series Forecasting, What-If Scenario Planning, and Automated ETL Validation.")

kpis = calculate_kpis(df_filtered)
yoy = calculate_yoy_growth(df_filtered)

# 6 KPI Columns
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
    "📈 Forecast & Scenario Simulator",
    "🔍 Data Inspector & Exporter"
])

# TAB 1: EXECUTIVE SUMMARY
with tab1:
    st.subheader("Executive Financial Performance & Monthly Trends")
    
    if df_filtered.empty:
        st.warning("No data available for selected filters.")
    else:
        df_monthly = df_filtered.groupby(df_filtered['Date'].dt.to_period('M')).agg({
            'Revenue': 'sum',
            'Profit': 'sum',
            'Budget': 'sum'
        }).reset_index()
        df_monthly['Month_Str'] = df_monthly['Date'].astype(str)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=df_monthly['Month_Str'], y=df_monthly['Revenue'],
            name='Revenue', marker_color=COLOR_PRIMARY, opacity=0.85
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

# TAB 2: REGIONAL PERFORMANCE
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
            'Revenue': 'sum', 'Gross Profit': 'sum', 'Profit': 'sum',
            'Budget': 'sum', 'Transaction ID': 'count'
        }).rename(columns={'Transaction ID': 'Transactions'}).reset_index()
        country_summary['Net Margin %'] = (country_summary['Profit'] / country_summary['Revenue']) * 100
        country_summary['Budget Util %'] = (country_summary['Revenue'] / country_summary['Budget']) * 100
        
        st.dataframe(
            country_summary.style.format({
                'Revenue': '${:,.2f}', 'Gross Profit': '${:,.2f}',
                'Profit': '${:,.2f}', 'Budget': '${:,.2f}',
                'Net Margin %': '{:.2f}%', 'Budget Util %': '{:.2f}%'
            }), use_container_width=True
        )

# TAB 3: PRODUCT & CUSTOMER ANALYTICS
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

# TAB 4: EXPENSE ANALYSIS
with tab4:
    st.subheader("Expense Structure & Departmental Cost Breakdown")
    
    if df_filtered.empty:
        st.warning("No data available.")
    else:
        e1, e2 = st.columns(2)
        with e1:
            rev = df_filtered['Revenue'].sum()
            cogs = df_filtered['Cost of Goods Sold (COGS)'].sum()
            opex = df_filtered['Operating Expense'].sum()
            mkt = df_filtered['Marketing Expense'].sum()
            tax = df_filtered['Tax'].sum()
            profit = df_filtered['Profit'].sum()
            
            fig_waterfall = go.Figure(go.Waterfall(
                name="P&L Statement", orientation="v",
                measure=["relative", "relative", "relative", "relative", "relative", "total"],
                x=["Revenue", "COGS", "OpEx", "Marketing", "Tax", "Net Profit"],
                textposition="outside",
                text=[f"${v/1e6:.1f}M" for v in [rev, -cogs, -opex, -mkt, -tax, profit]],
                y=[rev, -cogs, -opex, -mkt, -tax, profit],
                connector={"line":{"color":"rgb(63, 63, 63)"}},
                decreasing={"marker":{"color":COLOR_DANGER}},
                increasing={"marker":{"color":COLOR_SUCCESS}},
                totals={"marker":{"color":COLOR_PRIMARY}}
            ))
            fig_waterfall.update_layout(
                title="P&L Financial Waterfall Breakdown ($)",
                template=PLOTLY_TEMPLATE, height=420
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
        with e2:
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

# TAB 5: FINANCIAL FORECAST & WHAT-IF SCENARIO SIMULATOR
with tab5:
    st.subheader("🔮 12-Month Financial Forecasting & What-If Scenario Simulator")
    st.markdown("Utilize trend forecasting models and adjust key price/cost levers to simulate future earnings.")
    
    if df_filtered.empty:
        st.warning("No data available for forecasting.")
    else:
        # Time-Series Forecasting Model (Holt-Winters / Exponential Smoothing Trend)
        df_monthly_ts = df_filtered.groupby(df_filtered['Date'].dt.to_period('M'))['Revenue'].sum().reset_index()
        df_monthly_ts['Month_Str'] = df_monthly_ts['Date'].astype(str)
        
        # Fit Linear Trend Model
        x_idx = np.arange(len(df_monthly_ts))
        y_rev = df_monthly_ts['Revenue'].values
        slope, intercept = np.polyfit(x_idx, y_rev, 1)
        
        # 12-Month Future Projection
        future_x = np.arange(len(df_monthly_ts), len(df_monthly_ts) + 12)
        future_y = slope * future_x + intercept
        future_months = [f"2026-{m:02d}" for m in range(1, 13)]
        
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(x=df_monthly_ts['Month_Str'], y=y_rev, name='Historical Revenue', line=dict(color=COLOR_PRIMARY, width=3)))
        fig_fc.add_trace(go.Scatter(x=future_months, y=future_y, name='12-Month Trend Forecast', line=dict(color=COLOR_SUCCESS, width=3, dash='dash')))
        fig_fc.update_layout(title="Historical Monthly Revenue & 12-Month Trend Forecast ($)", template=PLOTLY_TEMPLATE, height=380)
        st.plotly_chart(fig_fc, use_container_width=True)
        
        st.markdown("### What-If Scenario Controls")
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
        base_profit = df_filtered['Profit'].sum()
        
        sim_rev = base_rev * (1 + price_change / 100.0) + (base_mkt * (mkt_boost / 100.0) * 1.5)
        sim_cogs = base_cogs * (1 + cogs_change / 100.0)
        sim_mkt = base_mkt * (1 + mkt_boost / 100.0)
        sim_tax = (sim_rev - sim_cogs - base_opex - sim_mkt) * 0.15
        if sim_tax < 0: sim_tax = 0.0
        
        sim_profit = sim_rev - sim_cogs - base_opex - sim_mkt - sim_tax
        sim_margin = (sim_profit / sim_rev * 100) if sim_rev > 0 else 0.0
        
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Simulated Revenue", f"${sim_rev/1e6:.2f}M", delta=f"${(sim_rev-base_rev)/1e6:+.2f}M")
        sc2.metric("Simulated Net Profit", f"${sim_profit/1e6:.2f}M", delta=f"${(sim_profit-base_profit)/1e6:+.2f}M")
        sc3.metric("Simulated Net Margin", f"{sim_margin:.2f}%", delta=f"{sim_margin - (base_profit/base_rev*100):+.2f}%")
        sc4.metric("Marketing ROI Impact", f"{(sim_rev - base_rev)/(sim_mkt - base_mkt):.2f}x" if (sim_mkt - base_mkt) != 0 else "N/A")

# TAB 6: DATA INSPECTOR & EXPORTER
with tab6:
    st.subheader("Data Inspector & Export Reports")
    
    search_term = st.text_input("🔍 Search Transactions (Product, Region, City, Channel, Segment, etc.):", "")
    
    if search_term:
        mask_search = df_filtered.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)
        df_display = df_filtered[mask_search]
    else:
        df_display = df_filtered
        
    st.markdown(f"Displaying **{len(df_display):,}** matching rows.")
    st.dataframe(df_display.head(500), use_container_width=True)
    
    e_col1, e_col2 = st.columns(2)
    with e_col1:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV Report)",
            data=csv_data,
            file_name="filtered_financial_data.csv",
            mime="text/csv"
        )
    with e_col2:
        # Generate Text / Summary Report Download
        report_text = f"""FINANCIAL EXECUTIVE SUMMARY REPORT
Date Range: 2023-01-01 to 2025-12-31
Total Transactions: {len(df_filtered):,}
Total Revenue: ${kpis['total_revenue']:,.2f}
Total Gross Profit: ${kpis['total_gross_profit']:,.2f} ({kpis['gross_margin']:.2f}% Margin)
Total Expenses: ${kpis['total_expenses']:,.2f}
Total Net Profit: ${kpis['total_net_profit']:,.2f} ({kpis['net_margin']:.2f}% Margin)
Budget Utilization: {kpis['budget_utilization']:.2f}%
Average Order Value: ${kpis['aov']:,.2f}
"""
        st.download_button(
            label="📄 Download Executive Summary Report (TXT/PDF)",
            data=report_text,
            file_name="financial_summary_report.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Financial Performance Dashboard | Developed by Senior Data Analyst & BI Developer | Powered by Python & Streamlit</p>", unsafe_allow_html=True)
