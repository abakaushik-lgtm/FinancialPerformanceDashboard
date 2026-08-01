# Power BI Dashboard Specification & Visual Blueprint

**Project Title**: Financial Performance Dashboard & Business Insights  
**Tool**: Power BI Desktop / Service  
**Author**: Senior Data Analyst & BI Developer  

---

## 1. Data Architecture & Data Model (Star Schema)

The dashboard is structured around an optimized **Star Schema** data model for maximum DAX query performance and seamless slicing across multiple dimensions.

### Fact & Dimension Tables
```text
                  +-------------------------+
                  |        Dim_Date         |
                  +-------------------------+
                  | Date (PK)               |
                  | Year, Quarter, Month    |
                  +------------+------------+
                               | 1:N
                               v
+------------------+    +---------------+    +-------------------+
|   Dim_Geography  | 1:N| Fact_Financial|1:N |    Dim_Product    |
+------------------+--->| _Transactions |<---|-------------------|
| Region, Country, |    +---------------+    | Category, Product |
| City             |            ^ 1:N        +-------------------+
+------------------+            |
                         +------+--------+
                         | Dim_Customer  |
                         +---------------+
                         | Segment,      |
                         | Channel, Dept |
                         +---------------+
```

### Data Modeling Relationships
1. `Dim_Date[Date]` (1) ──> `Fact_Financial_Transactions[transaction_date]` (N) [Single Direction Filter]
2. `Dim_Geography[City]` (1) ──> `Fact_Financial_Transactions[city]` (N)
3. `Dim_Product[Product Name]` (1) ──> `Fact_Financial_Transactions[product_name]` (N)
4. `Dim_Customer[Customer Segment]` (1) ──> `Fact_Financial_Transactions[customer_segment]` (N)

---

## 2. Power Query ETL Transformation Steps

```m
let
    // 1. Source CSV Connection
    Source = Csv.Document(File.Contents("C:\Financial_Performance_Dashboard\data\cleaned_financial_data.csv"),[Delimiter=",", Columns=31, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // 2. Type Casting
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{
        {"Transaction ID", type text}, {"Date", type date}, {"Year", Int64.Type},
        {"Revenue", type number}, {"Cost of Goods Sold (COGS)", type number},
        {"Operating Expense", type number}, {"Marketing Expense", type number},
        {"Tax", type number}, {"Profit", type number}, {"Budget", type number}
    }),
    
    // 3. Calculated Columns in Power Query
    AddGrossProfit = Table.AddColumn(ChangeTypes, "Gross Profit PQ", each [Revenue] - [#"Cost of Goods Sold (COGS)"], type number),
    AddNetProfitMargin = Table.AddColumn(AddGrossProfit, "Net Margin PQ", each ([Profit] / [Revenue]) * 100, type number)
in
    AddNetProfitMargin
```

---

## 3. Detailed 5-Page Dashboard Specification

### Page 1: Executive Summary 📊
* **Goal**: Provide high-level visibility for C-Suite executives on revenue, profit, expenses, and budget alignment.
* **Layout & Visuals**:
  1. **Header Banner**: Dynamic Title (`[Dynamic Executive Title]`), Slicer Panel (Year, Quarter, Region).
  2. **Top Row KPI Cards** (4 Cards):
     - **Card 1**: Total Revenue (`$366.57M`) with YoY Trend Badge (`+15.2%`).
     - **Card 2**: Total Net Profit (`$109.79M`) with Net Margin (`29.95%`).
     - **Card 3**: Total Expenses (`$256.78M`) with Cost Ratio (`70.05%`).
     - **Card 4**: Budget Utilization (`101.57%`) with Target Status Indicator.
  3. **Visual 1 (Main Combo Chart)**: Monthly Revenue & Profit Trend vs. Monthly Budget (Line & Clustered Column Chart).
  4. **Visual 2 (Bar Chart)**: Revenue & Profit by Business Unit.
  5. **Visual 3 (Waterfall Chart)**: Financial P&L Bridge (Revenue ──> COGS ──> OpEx ──> Marketing ──> Tax ──> Net Profit).

---

### Page 2: Regional Performance & Geography 🌍
* **Goal**: Analyze geographic revenue distribution, country-level margins, and top-performing cities.
* **Layout & Visuals**:
  1. **Visual 1 (Filled Map / Bubble Map)**: Global Revenue & Profit Margin Map by Country/City.
  2. **Visual 2 (Bar Chart)**: Revenue & Profit Margin % by Region (North America, Europe, APAC, LatAm, MEA).
  3. **Visual 3 (Matrix Grid)**: Country & City Hierarchy Table with Conditional Color Formatting on Profit Margin (Green > 30%, Red < 25%).
  4. **Visual 4 (Scatter Plot)**: Regional Volume (Transactions) vs. Average Order Value (AOV).

---

### Page 3: Product & Customer Analysis 📦
* **Goal**: Evaluate product portfolio profitability, category mix, customer segment contribution, and channel efficiency.
* **Layout & Visuals**:
  1. **Visual 1 (Treemap)**: Revenue Contribution % by Product Category (Software, Cloud, Hardware, Electronics, Consulting).
  2. **Visual 2 (Bar Chart)**: Top 10 Products by Revenue & Profit.
  3. **Visual 3 (Scatter Plot)**: Product Revenue vs. Profit Margin % (identifying high-revenue, low-margin products needing pricing adjustments).
  4. **Visual 4 (Donut Chart)**: Revenue Split by Sales Channel (Direct Sales, Online, Partner, Reseller).
  5. **Visual 5 (Clustered Column Chart)**: Customer Segment Spend (Enterprise vs. SMB vs. Mid-Market vs. Consumer).

---

### Page 4: Expense & Cost Structure Analysis 💸
* **Goal**: Audit expense distribution across departments and identify cost optimization levers.
* **Layout & Visuals**:
  1. **Visual 1 (Donut Chart)**: Overall Expense Breakdown (COGS, OpEx, Marketing, Tax).
  2. **Visual 2 (Stacked Bar Chart)**: Department-wise Operating & Marketing Expenses (Sales, Engineering, Operations, Marketing, Support).
  3. **Visual 3 (Line Chart)**: Monthly Marketing Expense vs. Revenue Growth Rate (evaluating marketing ROI).
  4. **Visual 4 (Table with Data Bars)**: Business Unit Cost Ratios & Variance Analysis.

---

### Page 5: Financial Forecast & Scenario Analysis 📈
* **Goal**: Provide forward-looking projections and interactive what-if scenario simulation for strategic planning.
* **Layout & Visuals**:
  1. **Visual 1 (Forecasting Chart)**: 12-Month Revenue & Profit Forecast (using Power BI Built-in Holt-Winters Exponential Smoothing with 95% Confidence Interval).
  2. **Interactive Slicers / Parameters**:
     - **Price Adjustment Parameter**: `-10%` to `+20%` slider.
     - **COGS Shift Parameter**: `-15%` to `+15%` slider.
  3. **Visual 2 (Dynamic Gauge & Card)**: Simulated Net Profit under selected scenario vs Baseline Net Profit.
  4. **Visual 3 (Scenario Comparison Chart)**: Baseline Revenue vs Simulated Revenue across Product Categories.

---

## 4. Advanced Power BI Features Implemented

* **DAX Measures**: 25+ measures using `CALCULATE`, `SAMEPERIODLASTYEAR`, `TOTALYTD`, `RANKX`, `DIVIDE`, and `SELECTEDVALUE`.
* **Drill Through**: Enabled Drill Through from Product Category in Page 3 down to detailed Transaction-level details page.
* **Bookmarks & Navigation Buttons**: Page Navigation Bar at top with custom icons, toggle buttons for switching views between Revenue and Profit.
* **Custom Tooltip Pages**: Hovering over any Regional Map location renders a pop-up micro-chart showing monthly trend and top product.
* **Conditional Formatting**: Background color scales on matrix tables for Profit Margin % and Budget Variance.
