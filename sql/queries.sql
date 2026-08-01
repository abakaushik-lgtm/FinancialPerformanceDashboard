-- ============================================================================
-- Financial Performance Dashboard - 30 Analytical SQL Business Queries
-- Database Engine: SQLite / PostgreSQL / ANSI SQL Compatible
-- Author: Senior Data Analyst & BI Developer
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 1: Monthly Revenue Trend
-- ----------------------------------------------------------------------------
SELECT 
    strftime('%Y-%m', transaction_date) AS year_month,
    year,
    month,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM financial_transactions
GROUP BY year_month, year, month
ORDER BY year_month ASC;

-- ----------------------------------------------------------------------------
-- QUERY 2: Monthly Net Profit & Margin % Trend
-- ----------------------------------------------------------------------------
SELECT 
    strftime('%Y-%m', transaction_date) AS year_month,
    year,
    month,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS net_profit_margin_pct
FROM financial_transactions
GROUP BY year_month, year, month
ORDER BY year_month ASC;

-- ----------------------------------------------------------------------------
-- QUERY 3: Top 10 Products by Total Revenue
-- ----------------------------------------------------------------------------
SELECT 
    product_category,
    product_name,
    COUNT(transaction_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM financial_transactions
GROUP BY product_category, product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- QUERY 4: Top Customer Segments & Spending Analysis
-- ----------------------------------------------------------------------------
SELECT 
    customer_segment,
    COUNT(transaction_id) AS transaction_count,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    ROUND(SUM(profit), 2) AS total_profit
FROM financial_transactions
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- QUERY 5: Region-wise Revenue Contribution %
-- ----------------------------------------------------------------------------
SELECT 
    region,
    COUNT(transaction_id) AS transaction_count,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) * 100.0 / (SELECT SUM(revenue) FROM financial_transactions), 2) AS revenue_share_pct
FROM financial_transactions
GROUP BY region
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- QUERY 6: Region-wise Profit & Regional Profit Margin %
-- ----------------------------------------------------------------------------
SELECT 
    region,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS regional_profit_margin_pct
FROM financial_transactions
GROUP BY region
ORDER BY total_profit DESC;

-- ----------------------------------------------------------------------------
-- QUERY 7: Highest Margin Products (> $1M Revenue)
-- ----------------------------------------------------------------------------
SELECT 
    product_name,
    product_category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS profit_margin_pct
FROM financial_transactions
GROUP BY product_name, product_category
HAVING total_revenue > 1000000
ORDER BY profit_margin_pct DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- QUERY 8: Lowest Margin Products (Margin Dilution Audit)
-- ----------------------------------------------------------------------------
SELECT 
    product_name,
    product_category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS profit_margin_pct
FROM financial_transactions
GROUP BY product_name, product_category
ORDER BY profit_margin_pct ASC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- QUERY 9: Average Monthly Revenue & Performance Benchmark (CTE)
-- ----------------------------------------------------------------------------
WITH monthly_sales AS (
    SELECT strftime('%Y-%m', transaction_date) AS ym, SUM(revenue) AS monthly_rev
    FROM financial_transactions GROUP BY ym
)
SELECT 
    ym,
    ROUND(monthly_rev, 2) AS monthly_revenue,
    ROUND((SELECT AVG(monthly_rev) FROM monthly_sales), 2) AS avg_monthly_benchmark,
    ROUND(monthly_rev - (SELECT AVG(monthly_rev) FROM monthly_sales), 2) AS variance_from_avg
FROM monthly_sales ORDER BY ym ASC;

-- ----------------------------------------------------------------------------
-- QUERY 10: Running Total (Cumulative) Revenue (Window Function: SUM OVER)
-- ----------------------------------------------------------------------------
WITH monthly_rev AS (
    SELECT strftime('%Y-%m', transaction_date) AS ym, SUM(revenue) AS revenue
    FROM financial_transactions GROUP BY ym
)
SELECT 
    ym,
    ROUND(revenue, 2) AS monthly_revenue,
    ROUND(SUM(revenue) OVER (ORDER BY ym ASC), 2) AS running_total_revenue
FROM monthly_rev;

-- ----------------------------------------------------------------------------
-- QUERY 11: Product Revenue Ranking by Category (Window Function: DENSE_RANK)
-- ----------------------------------------------------------------------------
WITH product_perf AS (
    SELECT product_category, product_name, SUM(revenue) AS total_revenue
    FROM financial_transactions GROUP BY product_category, product_name
)
SELECT 
    product_category,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue,
    DENSE_RANK() OVER (PARTITION BY product_category ORDER BY total_revenue DESC) AS rank_within_category
FROM product_perf;

-- ----------------------------------------------------------------------------
-- QUERY 12: Month-over-Month (MoM) Revenue Growth % (Window Function: LAG)
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- QUERY 13: Month-over-Month (MoM) Profit Growth %
-- ----------------------------------------------------------------------------
WITH monthly_p AS (
    SELECT strftime('%Y-%m', transaction_date) AS ym, SUM(profit) AS profit
    FROM financial_transactions GROUP BY ym
)
SELECT 
    ym,
    ROUND(profit, 2) AS current_month_profit,
    ROUND(LAG(profit, 1) OVER (ORDER BY ym ASC), 2) AS prev_month_profit,
    ROUND(((profit - LAG(profit, 1) OVER (ORDER BY ym ASC)) / LAG(profit, 1) OVER (ORDER BY ym ASC)) * 100, 2) AS mom_profit_growth_pct
FROM monthly_p;

-- ----------------------------------------------------------------------------
-- QUERY 14: Budget vs Actual Variance Analysis by Business Unit
-- ----------------------------------------------------------------------------
SELECT 
    business_unit,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(actual_sales), 2) AS total_actual_sales,
    ROUND(SUM(actual_sales) - SUM(budget), 2) AS budget_variance,
    ROUND((SUM(actual_sales) / SUM(budget)) * 100, 2) AS budget_utilization_pct
FROM financial_transactions
GROUP BY business_unit
ORDER BY budget_variance DESC;

-- ----------------------------------------------------------------------------
-- QUERY 15: Year-over-Year (YoY) Performance Comparison
-- ----------------------------------------------------------------------------
SELECT 
    year,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(cogs), 2) AS total_cogs,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS profit_margin_pct
FROM financial_transactions
GROUP BY year ORDER BY year ASC;

-- ----------------------------------------------------------------------------
-- QUERY 16: Quarter-wise Performance & QoQ Revenue Growth
-- ----------------------------------------------------------------------------
WITH qtr_perf AS (
    SELECT year, quarter, SUM(revenue) AS qtr_revenue, SUM(profit) AS qtr_profit
    FROM financial_transactions GROUP BY year, quarter
)
SELECT 
    year,
    quarter,
    ROUND(qtr_revenue, 2) AS qtr_revenue,
    ROUND(qtr_profit, 2) AS qtr_profit,
    ROUND(LAG(qtr_revenue, 1) OVER (ORDER BY year ASC, quarter ASC), 2) AS prev_qtr_revenue,
    ROUND(((qtr_revenue - LAG(qtr_revenue, 1) OVER (ORDER BY year ASC, quarter ASC)) / LAG(qtr_revenue, 1) OVER (ORDER BY year ASC, quarter ASC)) * 100, 2) AS qoq_growth_pct
FROM qtr_perf;

-- ----------------------------------------------------------------------------
-- QUERY 17: Department-wise Expenses Breakdown & Cost Ratios
-- ----------------------------------------------------------------------------
SELECT 
    department,
    ROUND(SUM(operating_expense), 2) AS total_operating_expense,
    ROUND(SUM(marketing_expense), 2) AS total_marketing_expense,
    ROUND(SUM(operating_expense + marketing_expense), 2) AS total_dept_expenses,
    ROUND((SUM(operating_expense + marketing_expense) / (SELECT SUM(revenue) FROM financial_transactions)) * 100, 2) AS expense_to_total_rev_pct
FROM financial_transactions
GROUP BY department ORDER BY total_dept_expenses DESC;

-- ----------------------------------------------------------------------------
-- QUERY 18: Customer Segment Profitability Matrix
-- ----------------------------------------------------------------------------
SELECT 
    customer_segment,
    sales_channel,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS margin_pct
FROM financial_transactions
GROUP BY customer_segment, sales_channel
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- QUERY 19: Sales Channel Revenue & Discount Efficiency
-- ----------------------------------------------------------------------------
SELECT 
    sales_channel,
    ROUND(SUM(revenue), 2) AS gross_revenue,
    ROUND(SUM(discount), 2) AS total_discounts,
    ROUND((SUM(discount) / SUM(revenue)) * 100, 2) AS avg_discount_pct,
    ROUND(SUM(profit), 2) AS net_profit
FROM financial_transactions
GROUP BY sales_channel ORDER BY gross_revenue DESC;

-- ----------------------------------------------------------------------------
-- QUERY 20: Profit Margin % by Product Category
-- ----------------------------------------------------------------------------
SELECT 
    product_category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(cogs), 2) AS total_cogs,
    ROUND(SUM(gross_profit), 2) AS total_gross_profit,
    ROUND((SUM(gross_profit) / SUM(revenue)) * 100, 2) AS gross_margin_pct,
    ROUND(SUM(profit), 2) AS total_net_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS net_margin_pct
FROM financial_transactions
GROUP BY product_category ORDER BY net_margin_pct DESC;

-- ----------------------------------------------------------------------------
-- QUERY 21: Best Performing Month (Highest Net Profit Margin)
-- ----------------------------------------------------------------------------
SELECT 
    strftime('%Y-%m', transaction_date) AS year_month,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS margin_pct
FROM financial_transactions
GROUP BY year_month ORDER BY margin_pct DESC LIMIT 1;

-- ----------------------------------------------------------------------------
-- QUERY 22: Worst Performing Month (Lowest Total Revenue)
-- ----------------------------------------------------------------------------
SELECT 
    strftime('%Y-%m', transaction_date) AS year_month,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS margin_pct
FROM financial_transactions
GROUP BY year_month ORDER BY total_revenue ASC LIMIT 1;

-- ----------------------------------------------------------------------------
-- QUERY 23: Pareto 80/20 Revenue Contribution per Category (Window SUM OVER)
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- QUERY 24: 3-Month Moving Average Revenue (Window Function: AVG OVER)
-- ----------------------------------------------------------------------------
WITH monthly_rev AS (
    SELECT strftime('%Y-%m', transaction_date) AS ym, SUM(revenue) AS revenue
    FROM financial_transactions GROUP BY ym
)
SELECT 
    ym,
    ROUND(revenue, 2) AS monthly_revenue,
    ROUND(AVG(revenue) OVER (ORDER BY ym ASC ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m_revenue
FROM monthly_rev;

-- ----------------------------------------------------------------------------
-- QUERY 25: Q3 Marketing Efficiency Audit (Expense vs Profit Margin Dip)
-- ----------------------------------------------------------------------------
SELECT 
    quarter,
    year,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(marketing_expense), 2) AS marketing_expense,
    ROUND((SUM(marketing_expense) / SUM(revenue)) * 100, 2) AS mkt_to_rev_pct,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS net_profit_margin_pct
FROM financial_transactions
GROUP BY quarter, year
ORDER BY year ASC, quarter ASC;

-- ----------------------------------------------------------------------------
-- QUERY 26: High-Revenue Low-Margin Product Flagging
-- ----------------------------------------------------------------------------
SELECT 
    product_name,
    product_category,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS net_margin_pct
FROM financial_transactions
GROUP BY product_name, product_category
HAVING revenue > 20000000 AND net_margin_pct < 15.0
ORDER BY net_margin_pct ASC;

-- ----------------------------------------------------------------------------
-- QUERY 27: Executive View 1 - KPI Summary View Creation
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS v_executive_kpi_summary;
CREATE VIEW v_executive_kpi_summary AS
SELECT 
    year,
    quarter,
    COUNT(transaction_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(cogs), 2) AS total_cogs,
    ROUND(SUM(operating_expense + marketing_expense), 2) AS total_opex,
    ROUND(SUM(profit), 2) AS total_net_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(actual_sales) - SUM(budget), 2) AS budget_variance
FROM financial_transactions
GROUP BY year, quarter;

-- ----------------------------------------------------------------------------
-- QUERY 28: Executive View 2 - Regional Performance Hierarchy
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS v_regional_performance;
CREATE VIEW v_regional_performance AS
SELECT 
    region,
    country,
    city,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS profit_margin_pct
FROM financial_transactions
GROUP BY region, country, city;

-- ----------------------------------------------------------------------------
-- QUERY 29: Executive View 3 - Product Profitability Matrix
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS v_product_profitability;
CREATE VIEW v_product_profitability AS
SELECT 
    product_category,
    product_name,
    COUNT(transaction_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(gross_profit), 2) AS total_gross_profit,
    ROUND(SUM(profit), 2) AS total_net_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS net_margin_pct
FROM financial_transactions
GROUP BY product_category, product_name;

-- ----------------------------------------------------------------------------
-- QUERY 30: Executive View 4 - Monthly Trend & Growth View
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS v_monthly_trend_forecast;
CREATE VIEW v_monthly_trend_forecast AS
SELECT 
    year,
    month,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_net_profit,
    ROUND(SUM(budget), 2) AS total_budget
FROM financial_transactions
GROUP BY year, month;
