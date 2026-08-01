# Financial Performance Dashboard & Business Insights 📊💸

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-DAX_%26_PowerQuery-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive_Visuals-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end enterprise-grade **Financial Performance Dashboard & Business Analytics Suite** built with **Python, SQL, Power BI, and Streamlit**. This repository provides complete data cleaning pipelines, statistical EDA, an SQLite database with 25+ analytical SQL queries (CTEs, Window Functions, Views), a 25+ DAX measure library, a 5-page Power BI blueprint, an interactive dark-mode Streamlit executive application with what-if scenario forecasting, and an executive report with 25+ actionable business insights.

---

## 📌 Problem Statement & Project Objective

Management requires clear, real-time visibility into multi-dimensional financial performance across global regions, business units, product categories, and sales channels. Manual spreadsheet tracking creates data quality issues, delayed insights, and limited scenario modeling capabilities.

**Objective**: Develop a production-ready, interactive financial analytics ecosystem that enables stakeholders to:
1. Track core metrics (**Revenue, COGS, OpEx, Net Profit, Gross Margin %, Budget Variance**).
2. Clean and audit 12,000+ raw transactional records.
3. Run complex business queries using SQL window functions, CTEs, and views.
4. Visualize performance in Power BI and Streamlit with interactive filtering and scenario planning.
5. Derive 25+ actionable business recommendations to optimize revenue and cost structures.

---

## 🏗️ Repository Architecture & Directory Structure

```text
Financial_Performance_Dashboard/
│
├── data/
│   ├── raw_financial_data.csv        # 12,000+ synthetic raw transactions (with deliberate anomalies)
│   ├── cleaned_financial_data.csv    # Deduplicated, imputed, outlier-capped & engineered dataset
│   └── financial_db.sqlite           # SQLite database table & executive views
│
├── sql/
│   ├── schema.sql                    # DDL table creation script & indexes
│   ├── queries.sql                   # 25+ production business SQL queries (CTEs, Window Functions, Views)
│   └── build_db.py                   # Automated database build & verification pipeline
│
├── notebooks/
│   ├── 01_data_cleaning.py           # Python data cleaning routine (IQR outlier capping, dtypes, KPIs)
│   └── 02_eda.py                     # Exploratory Data Analysis & statistical summaries
│
├── powerbi/
│   ├── dax_measures.dax              # 25+ DAX metrics (YoY Growth, YTD, Budget Variance, Ranks)
│   └── powerbi_guide.md              # 5-Page Dashboard visual blueprint & Power Query M setup
│
├── streamlit/
│   ├── app.py                        # Streamlit sub-wrapper
│   ├── kpi_engine.py                 # Financial KPI calculation engine
│   └── styles.css                    # Glassmorphism dark mode UI stylesheet
│
├── reports/
│   └── business_insights.md          # 25+ Detailed executive business insights & strategic recommendations
│
├── app.py                            # Main Streamlit web application entry point
├── requirements.txt                  # Python dependencies
├── LICENSE                           # MIT License
└── README.md                         # Portfolio documentation & ATS resume bullets
```

---

## 🔑 Key Financial Performance Indicators (KPIs)

Analyzing **12,000 global transactions** spanning 2023–2025:

| Financial Metric | Total Value ($) | Margin / Benchmark | YoY Growth / Variance |
| :--- | :---: | :---: | :---: |
| **Total Revenue** | **$366.57M** | 100.0% | **+15.24% YoY (2025)** |
| **Gross Profit** | **$216.04M** | **58.93% Gross Margin** | Healthy COGS control |
| **Total Expenses** | **$256.78M** | **70.05% Cost Ratio** | COGS + OpEx + Marketing + Tax |
| **Net Profit** | **$109.79M** | **29.95% Net Margin** | $41.79M in FY2025 |
| **Budget Target** | **$360.92M** | **101.57% Utilization** | **+$5.65M Surplus** |
| **Average Order Value (AOV)** | **$30,517** | 12,000 Txns | Enterprise contract size |

---

## 🧹 1. Python Data Cleaning Pipeline (`notebooks/01_data_cleaning.py`)

The raw dataset (`data/raw_financial_data.csv`) contains intentional real-world anomalies:
* **Missing Values**: Imputed categorical fields (`Customer Segment`) with mode and numerical fields (`Marketing Expense`) with category medians.
* **Deduplication**: Identified and removed duplicate rows based on unique `Transaction ID`.
* **Outlier Treatment**: Applied conservative **Interquartile Range (IQR 3x)** capping to handle extreme data entry spikes in `Revenue` and `Operating Expense`.
* **Standardization**: Trimmed white space, title-cased regions/countries, and preserved enterprise acronyms (`SaaS`, `ERP`, `AI`, `SMB`, `USA`).
* **Feature Engineering**: Engineered calculated columns: `Gross Profit`, `Operating Profit`, `Net Profit`, `Gross Margin %`, `Net Margin %`, `Budget Variance`, and `Cost Ratio %`.

---

## 🗄️ 2. SQL Analytics Engine (`sql/queries.sql`)

The database contains 25+ analytical SQL queries executed against SQLite (`data/financial_db.sqlite`):

### Featured SQL Examples

#### 1. Month-over-Month (MoM) Revenue Growth % (`LAG() OVER`)
```sql
WITH monthly AS (
    SELECT strftime('%Y-%m', transaction_date) AS ym, SUM(revenue) AS revenue
    FROM financial_transactions GROUP BY ym
)
SELECT 
    ym,
    ROUND(revenue, 2) AS current_month_revenue,
    ROUND(LAG(revenue, 1) OVER (ORDER BY ym ASC), 2) AS prev_month_revenue,
    ROUND(((revenue - LAG(revenue, 1) OVER (ORDER BY ym ASC)) / LAG(revenue, 1) OVER (ORDER BY ym ASC)) * 100, 2) AS mom_growth_pct
FROM monthly;
```

#### 2. Category Revenue Contribution % & Pareto Analysis
```sql
WITH cat_rev AS (
    SELECT product_category, SUM(revenue) AS category_revenue
    FROM financial_transactions GROUP BY product_category
)
SELECT 
    product_category,
    ROUND(category_revenue, 2) AS category_revenue,
    ROUND((category_revenue / (SELECT SUM(category_revenue) FROM cat_rev)) * 100, 2) AS revenue_contribution_pct,
    ROUND(SUM(category_revenue) OVER (ORDER BY category_revenue DESC) / (SELECT SUM(category_revenue) FROM cat_rev) * 100, 2) AS cumulative_contribution_pct
FROM cat_rev ORDER BY category_revenue DESC;
```

---

## 📊 3. Power BI Dashboard Blueprint & DAX Suite (`powerbi/`)

### Star Schema Architecture
* **Fact Table**: `Fact_Financial_Transactions`
* **Dimension Tables**: `Dim_Date`, `Dim_Geography`, `Dim_Product`, `Dim_Customer`

### 5-Page Dashboard Specification
1. **Page 1: Executive Summary**: KPI Cards, Revenue vs Profit Trend Combo Chart, Budget Variance.
2. **Page 2: Regional Analysis**: Global Map, Regional Revenue & Margin split, Top Cities bar chart.
3. **Page 3: Product Analysis**: Category Revenue Treemap, Top 10 Products, Profit Margin scatter plot.
4. **Page 4: Expense Analysis**: Financial P&L Waterfall chart, Department Expense distribution.
5. **Page 5: Financial Forecast**: Holt-Winters 12-Month Forecast & What-If Scenario Sliders.

---

## 🌐 4. Interactive Streamlit Web App (`app.py`)

The Streamlit web application delivers a modern dark glassmorphism dashboard:

### Core App Features
* **Global Sidebar Filters**: Year, Quarter, Region, Product Category, Business Unit, Department, Sales Channel, and Segment.
* **Real-Time KPI Cards**: Dynamic metrics with delta indicators (Revenue, Gross Profit, Expenses, Net Profit, Budget Target, AOV).
* **5 Interactive View Tabs**:
  - 📊 *Executive Summary*: Monthly Revenue & Profit Trend vs. Budget, Business Unit Variance.
  - 🌍 *Regional Performance*: Regional revenue bars, Top 10 Cities, Country financial matrix.
  - 📦 *Product & Customer*: Category Treemap, Top Products, Revenue vs Margin Scatter, Channel breakdown.
  - 💸 *Expense Analysis*: Financial P&L Waterfall breakdown, Departmental OpEx vs Marketing expenses.
  - 📈 *What-If Scenario Simulator*: Real-time sliders for Price Adjustment %, COGS Shift %, and Marketing Spend to model Net Profit impacts.
* **Data Inspector & CSV Exporter**: Live text search across all 12,000 records and instant CSV download button.

---

## 💡 5. Business Insights Highlights (`reports/business_insights.md`)

1. **North America Revenue Engine**: Generated **$127.89M (34.89% of global revenue)** with a **29.60% net margin**.
2. **Software Services High Margin**: Delivered **$111.17M in revenue** with an extraordinary **46.50% net margin** ($51.69M profit).
3. **Hardware Margin Dilution**: Hardware generated **$99.82M in revenue** but yielded only a **14.56% net margin** due to component COGS.
4. **Q4 Seasonality Surge**: December 2025 recorded peak revenue (**$14.72M**), benefiting from Q4 enterprise IT budget flushes.
5. **Budget Attainment**: Actual sales (**$366.57M**) exceeded budget targets (**$360.92M**) by **+$5.65M (+1.57% surplus)**.

---

## 📄 6. ATS-Friendly Resume Points

Highlight these quantified bullet points on your Data Analyst / Business Intelligence Developer resume:

* **Engineered an end-to-end Financial Performance Dashboard** using **Python, SQL, Power BI, and Streamlit**, analyzing **$366.57M in revenue** across **12,000+ global transactions** spanning 2023–2025.
* **Automated Python data cleaning pipeline** using Pandas and NumPy; processed raw transactional datasets by imputing missing values, removing duplicate records, and applying **3x IQR outlier capping** to ensure 100% data integrity.
* **Designed an SQLite relational database and wrote 25+ advanced business SQL queries** leveraging **CTEs, Window Functions (`RANK`, `SUM OVER`, `LAG`), and Views** to evaluate Month-over-Month (MoM) growth, Pareto revenue contribution, and budget variance.
* **Developed a 25+ DAX measure library in Power BI**, modeling Star Schema relationships, time-intelligence functions (`TOTALYTD`, `SAMEPERIODLASTYEAR`), dynamic titles, drill-through pages, and conditional formatting.
* **Built an interactive dark-mode Streamlit web application** featuring Plotly charts, dynamic multi-dimensional sidebar filters, P&L waterfall charts, and a real-time **What-If Scenario Simulator** for revenue and price elasticity forecasting.
* **Synthesized 25+ executive business insights and strategic recommendations**, identifying a **46.5% net profit margin in Software Services** and highlighting hardware cost-optimization opportunities to management.

---

## 🚀 7. Installation & Local Setup Guide

### Prerequisites
* Python 3.10 or higher
* Git

### Step-by-Step Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Financial_Performance_Dashboard.git
   cd Financial_Performance_Dashboard
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Data Generation & Cleaning Pipeline**
   ```bash
   python notebooks/01_data_cleaning.py
   ```

5. **Run SQL Database Build & Query Verification**
   ```bash
   python sql/build_db.py
   ```

6. **Launch Streamlit Web Application**
   ```bash
   streamlit run app.py
   ```

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.
