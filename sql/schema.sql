-- ============================================================================
-- Financial Performance Dashboard - Database Schema & Data Definition (DDL)
-- Database Engine: SQLite / ANSI SQL Compatible
-- Author: Senior Data Analyst & BI Developer
-- ============================================================================

DROP TABLE IF EXISTS financial_transactions;

CREATE TABLE financial_transactions (
    transaction_id TEXT PRIMARY KEY,
    transaction_date DATE NOT NULL,
    month TEXT NOT NULL,
    quarter TEXT NOT NULL,
    year INTEGER NOT NULL,
    region TEXT NOT NULL,
    country TEXT NOT NULL,
    city TEXT NOT NULL,
    business_unit TEXT NOT NULL,
    department TEXT NOT NULL,
    product_category TEXT NOT NULL,
    product_name TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    sales_channel TEXT NOT NULL,
    revenue REAL NOT NULL,
    cogs REAL NOT NULL,
    operating_expense REAL NOT NULL,
    marketing_expense REAL NOT NULL,
    discount REAL NOT NULL,
    tax REAL NOT NULL,
    profit REAL NOT NULL,
    profit_margin REAL NOT NULL,
    budget REAL NOT NULL,
    actual_sales REAL NOT NULL,
    gross_profit REAL NOT NULL,
    operating_profit REAL NOT NULL,
    gross_margin REAL NOT NULL,
    budget_variance REAL NOT NULL,
    budget_utilization REAL NOT NULL,
    total_expense REAL NOT NULL,
    cost_ratio REAL NOT NULL
);

-- Optimization Indexes
CREATE INDEX idx_txn_date ON financial_transactions(transaction_date);
CREATE INDEX idx_region_country ON financial_transactions(region, country);
CREATE INDEX idx_product_cat ON financial_transactions(product_category, product_name);
CREATE INDEX idx_year_quarter ON financial_transactions(year, quarter);
CREATE INDEX idx_cust_segment ON financial_transactions(customer_segment);
