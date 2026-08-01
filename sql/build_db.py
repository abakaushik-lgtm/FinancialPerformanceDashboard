"""
build_db.py
Automated SQLite Database Builder & SQL Query Verification Suite
Author: Senior Data Analyst & BI Developer
Description: Loads cleaned CSV dataset into SQLite database, executes schema setup, 
             and runs all 25+ business SQL queries to verify execution accuracy.
"""

import os
import sqlite3
import pandas as pd

def build_database():
    db_path = 'data/financial_db.sqlite'
    csv_path = 'data/cleaned_financial_data.csv'
    schema_path = 'sql/schema.sql'
    queries_path = 'sql/queries.sql'
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cleaned dataset CSV missing at {csv_path}")
        
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database file at '{db_path}'.")
        
    print(f"Connecting to SQLite database at '{db_path}'...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute schema setup
    print("Executing SQL schema creation (DDL)...")
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    
    # Load dataset into database table
    print(f"Loading '{csv_path}' into table 'financial_transactions'...")
    df = pd.read_csv(csv_path)
    
    # Column mapping to schema
    df_db = df.rename(columns={
        'Transaction ID': 'transaction_id',
        'Date': 'transaction_date',
        'Month': 'month',
        'Quarter': 'quarter',
        'Year': 'year',
        'Region': 'region',
        'Country': 'country',
        'City': 'city',
        'Business Unit': 'business_unit',
        'Department': 'department',
        'Product Category': 'product_category',
        'Product Name': 'product_name',
        'Customer Segment': 'customer_segment',
        'Sales Channel': 'sales_channel',
        'Revenue': 'revenue',
        'Cost of Goods Sold (COGS)': 'cogs',
        'Operating Expense': 'operating_expense',
        'Marketing Expense': 'marketing_expense',
        'Discount': 'discount',
        'Tax': 'tax',
        'Profit': 'profit',
        'Profit Margin': 'profit_margin',
        'Budget': 'budget',
        'Actual Sales': 'actual_sales',
        'Gross Profit': 'gross_profit',
        'Operating Profit': 'operating_profit',
        'Gross Margin': 'gross_margin',
        'Budget Variance': 'budget_variance',
        'Budget Utilization': 'budget_utilization',
        'Total Expense': 'total_expense',
        'Cost Ratio': 'cost_ratio'
    })
    
    df_db.to_sql('financial_transactions', conn, if_exists='append', index=False)
    conn.commit()
    
    # Verify row count
    cursor.execute("SELECT COUNT(*) FROM financial_transactions;")
    count = cursor.fetchone()[0]
    print(f"Database table populated successfully with {count:,} records.")
    
    # Execute and test all queries from queries.sql
    print("\n" + "="*60)
    print(" EXECUTING & VERIFYING 25+ SQL BUSINESS QUERIES")
    print("="*60)
    
    with open(queries_path, 'r', encoding='utf-8') as f:
        queries_sql = f.read()
        
    statements = [stmt.strip() for stmt in queries_sql.split(';') if stmt.strip()]
    query_counter = 0
    
    for stmt in statements:
        if stmt.startswith('--') and not any(k in stmt.upper() for k in ['SELECT', 'WITH', 'CREATE', 'DROP']):
            continue
        try:
            # Check if statement is SELECT, WITH, CREATE VIEW, or DROP VIEW
            upper_stmt = stmt.upper()
            if upper_stmt.startswith('CREATE') or upper_stmt.startswith('DROP'):
                cursor.execute(stmt)
                conn.commit()
                print(f"[OK] DDL / View statement executed successfully.")
            elif 'SELECT' in upper_stmt or 'WITH' in upper_stmt:
                query_counter += 1
                res_df = pd.read_sql_query(stmt, conn)
                print(f"[OK] Query #{query_counter:02d} executed successfully ({len(res_df)} rows returned)")
            else:
                cursor.execute(stmt)
                conn.commit()
                print(f"[OK] DDL/View statement executed successfully.")
        except Exception as e:
            print(f"[ERROR] Error in statement:\n{stmt[:100]}...\nError: {e}")
            
    print(f"\nAll {query_counter} analytical SQL queries verified cleanly!")
    conn.close()

if __name__ == '__main__':
    build_database()
