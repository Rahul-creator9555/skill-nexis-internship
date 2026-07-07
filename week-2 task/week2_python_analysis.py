"""
Week 2 - Python for Data Analysis
Dataset: sales_data.csv (200 rows, derived from SQL_Sales_Dataset_200_Rows.xlsx)

Covers all 5 practice tasks:
1. Load a CSV file using Pandas and display basic info.
2. Handle missing values and duplicates using Pandas.
3. Group data by category and find total revenue.
4. Sort data by multiple columns using Python.
5. Create a correlation matrix for numerical columns.
"""

import pandas as pd

pd.set_option('display.width', 120)
pd.set_option('display.max_columns', None)


def section(title):
    print('\n' + '=' * 70)
    print(title)
    print('=' * 70)


# ---------------------------------------------------------------
# 1. Load a CSV file using Pandas and display basic info
# ---------------------------------------------------------------
section('1. LOAD CSV & BASIC INFO')

df = pd.read_csv('sales_data.csv', parse_dates=['order_date'])

print('\nShape (rows, columns):', df.shape)

print('\nFirst 5 rows:')
print(df.head())

print('\nColumn info (df.info()):')
df.info()

print('\nSummary statistics (df.describe()):')
print(df.describe(include='all').transpose())


# ---------------------------------------------------------------
# 2. Handle missing values and duplicates using Pandas
# ---------------------------------------------------------------
section('2. MISSING VALUES & DUPLICATES')

print('\nMissing values per column:')
print(df.isnull().sum())

n_dupes = df.duplicated().sum()
print(f'\nFully duplicate rows found: {n_dupes}')

# General-purpose cleaning routine (works even if this run has none):
# - drop exact duplicate rows
# - fill missing numeric columns with the column median
# - fill missing text columns with 'Unknown'
df_clean = df.drop_duplicates().copy()

numeric_cols = df_clean.select_dtypes(include='number').columns
text_cols = df_clean.select_dtypes(exclude='number').columns.drop('order_date')

for col in numeric_cols:
    if df_clean[col].isnull().any():
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())

for col in text_cols:
    if df_clean[col].isnull().any():
        df_clean[col] = df_clean[col].fillna('Unknown')

print(f'\nRows before cleaning: {len(df)} | Rows after cleaning: {len(df_clean)}')
print('Missing values after cleaning:', df_clean.isnull().sum().sum())


# ---------------------------------------------------------------
# 3. Group data by category and find total revenue
# ---------------------------------------------------------------
section('3. TOTAL REVENUE BY CATEGORY')

revenue_by_category = (
    df_clean.groupby('category')['total_price']
    .sum()
    .sort_values(ascending=False)
    .rename('total_revenue')
)
print('\nTotal revenue by category:')
print(revenue_by_category)

# Bonus: also show average order value and order count per category
category_summary = df_clean.groupby('category').agg(
    total_revenue=('total_price', 'sum'),
    avg_order_value=('total_price', 'mean'),
    order_count=('order_id', 'count'),
).sort_values('total_revenue', ascending=False)
print('\nFull category summary:')
print(category_summary)


# ---------------------------------------------------------------
# 4. Sort data by multiple columns using Python
# ---------------------------------------------------------------
section('4. SORT BY MULTIPLE COLUMNS')

# Sort by category (A-Z) then total_price (highest first) within each category
sorted_df = df_clean.sort_values(by=['category', 'total_price'], ascending=[True, False])
print('\nTop 3 highest-value orders within each category (sorted by category, then total_price desc):')
print(sorted_df.groupby('category').head(3)[
    ['order_id', 'category', 'product_name', 'total_price']
])


# ---------------------------------------------------------------
# 5. Create a correlation matrix for numerical columns
# ---------------------------------------------------------------
section('5. CORRELATION MATRIX')

numeric_df = df_clean.select_dtypes(include='number').drop(columns=['order_id'])
corr_matrix = numeric_df.corr()
print('\nCorrelation matrix (quantity, unit_price, total_price):')
print(corr_matrix)

print('\nKey takeaway: total_price correlates strongly with both quantity and unit_price '
      'since total_price = quantity * unit_price by construction.')

section('DONE')
