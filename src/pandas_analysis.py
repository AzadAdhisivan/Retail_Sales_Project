"""
pandas_analysis.py
Part 2 - Pandas Tasks:
  - Data cleaning (missing values, outliers, dtypes, dates)
  - EDA: sales by region/month, top products, profit breakdown
"""

import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_csv

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_PATH = os.path.join(BASE_DIR, "data", "cleaned_superstore.csv")


# ── 1. Load into DataFrame ────────────────────────────────────────────────────
def load_dataframe():
    rows = load_csv()
    df   = pd.DataFrame(rows)
    return df


# ── 2. Data Cleaning ──────────────────────────────────────────────────────────
def clean_dataframe(df):
    print("\n🧹 Data Cleaning:")

    # Fix data types
    df["Sales"]    = pd.to_numeric(df["Sales"])
    df["Profit"]   = pd.to_numeric(df["Profit"])
    df["Discount"] = pd.to_numeric(df["Discount"])
    df["Quantity"] = pd.to_numeric(df["Quantity"])

    # Standardize date formats
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"])

    # Check missing values
    missing = df.isnull().sum()
    print(f"   Missing values per column:\n{missing[missing > 0]}")
    if missing.sum() == 0:
        print("   No missing values found ✅")

    # Handle outliers in Sales using IQR method
    Q1  = df["Sales"].quantile(0.25)
    Q3  = df["Sales"].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df["Sales"] < lower) | (df["Sales"] > upper)]
    print(f"\n   Sales outliers detected  : {len(outliers)} rows")
    print(f"   Normal sales range       : ${lower:.2f} to ${upper:.2f}")

    # Flag outliers instead of dropping them
    df["Sales_Outlier"] = (df["Sales"] < lower) | (df["Sales"] > upper)

    # Add helper columns
    df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Order Year"]  = df["Order Date"].dt.year

    print(f"\n   Final DataFrame shape    : {df.shape}")
    print(f"   Columns                  : {list(df.columns)}")

    return df


# ── 3. Sales Trends by Region ─────────────────────────────────────────────────
def sales_by_region(df):
    print("\n🌍 Sales by Region:")
    region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False).round(2)
    for r, s in region.items():
        print(f"   {r:<12} ${s:,.2f}")
    return region


# ── 4. Sales Trends by Month ──────────────────────────────────────────────────
def sales_by_month(df):
    print("\n📅 Sales by Month (all years combined):")
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Month Num"]  = df["Order Date"].dt.month
    monthly = df.groupby(["Month Num", "Month Name"])["Sales"].sum()
    monthly = monthly.reset_index().sort_values("Month Num")
    for _, row in monthly.iterrows():
        print(f"   {row['Month Name']:<5} ${row['Sales']:,.2f}")
    return monthly


# ── 5. Top 10 Profitable Products ────────────────────────────────────────────
def top_profitable_products(df):
    print("\n🏆 Top 10 Profitable Products:")
    top = df.groupby("Product Name")["Profit"].sum().sort_values(ascending=False).head(10).round(2)
    for i, (name, profit) in enumerate(top.items(), 1):
        print(f"   {i:>2}. {name[:50]:<50} ${profit:,.2f}")
    return top


# ── 6. Profit by Category ─────────────────────────────────────────────────────
def profit_by_category(df):
    print("\n📦 Profit by Category:")
    cat = df.groupby("Category")["Profit"].sum().sort_values(ascending=False).round(2)
    for c, p in cat.items():
        print(f"   {c:<20} ${p:,.2f}")
    return cat


# ── 7. Profit by Segment ──────────────────────────────────────────────────────
def profit_by_segment(df):
    print("\n👤 Profit by Segment:")
    seg = df.groupby("Segment")["Profit"].sum().sort_values(ascending=False).round(2)
    for s, p in seg.items():
        print(f"   {s:<15} ${p:,.2f}")
    return seg


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_dataframe()
    df = clean_dataframe(df)

    sales_by_region(df)
    sales_by_month(df)
    top_profitable_products(df)
    profit_by_category(df)
    profit_by_segment(df)

    # Save cleaned DataFrame
    df.to_csv(CLEANED_PATH, index=False)
    print(f"\n💾 Cleaned DataFrame saved to: {CLEANED_PATH}")