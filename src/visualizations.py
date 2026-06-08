"""
visualizations.py
Part 2 - Visual report using matplotlib and seaborn.
Charts saved to reports/
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pandas_analysis import load_dataframe, clean_dataframe

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR  = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Global style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120


# ── 1. Bar Chart — Sales by Region ───────────────────────────────────────────
def plot_sales_by_region(df):
    region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(region.index, region.values, color=sns.color_palette("muted", len(region)))
    ax.set_title("Total Sales by Region", fontsize=14, fontweight="bold")
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 5000,
                f"${bar.get_height():,.0f}",
                ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "sales_by_region.png")
    plt.savefig(path)
    plt.close()
    print(f"   ✅ Saved: sales_by_region.png")


# ── 2. Line Chart — Monthly Sales Trend ──────────────────────────────────────
def plot_monthly_sales(df):
    df["Month"]     = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    monthly = df.groupby(["Month", "Month Name"])["Sales"].sum().reset_index().sort_values("Month")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["Month Name"], monthly["Sales"], marker="o", linewidth=2, color="#4C72B0")
    ax.fill_between(monthly["Month Name"], monthly["Sales"], alpha=0.15, color="#4C72B0")
    ax.set_title("Monthly Sales Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "monthly_sales_trend.png")
    plt.savefig(path)
    plt.close()
    print(f"   ✅ Saved: monthly_sales_trend.png")


# ── 3. Horizontal Bar — Top 10 Profitable Products ───────────────────────────
def plot_top_products(df):
    top = df.groupby("Product Name")["Profit"].sum().sort_values(ascending=True).tail(10)
    labels = [name[:40] for name in top.index]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(labels, top.values, color=sns.color_palette("Blues_d", len(top)))
    ax.set_title("Top 10 Profitable Products", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Profit ($)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    for bar in bars:
        ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height() / 2,
                f"${bar.get_width():,.0f}", va="center", fontsize=8)

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "top_profitable_products.png")
    plt.savefig(path)
    plt.close()
    print(f"   ✅ Saved: top_profitable_products.png")


# ── 4. Heatmap — Profit by Category and Region ───────────────────────────────
def plot_heatmap(df):
    pivot = df.pivot_table(values="Profit", index="Category", columns="Region", aggfunc="sum").round(0)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu",
                linewidths=0.5, ax=ax, cbar_kws={"label": "Profit ($)"})
    ax.set_title("Profit by Category and Region", fontsize=14, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "profit_heatmap.png")
    plt.savefig(path)
    plt.close()
    print(f"   ✅ Saved: profit_heatmap.png")


# ── 5. Scatter Plot — Sales vs Profit ────────────────────────────────────────
def plot_sales_vs_profit(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    scatter = ax.scatter(df["Sales"], df["Profit"],
                         c=df["Discount"], cmap="coolwarm",
                         alpha=0.4, s=15)

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Discount Rate")
    ax.set_title("Sales vs Profit (colored by Discount)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Sales ($)")
    ax.set_ylabel("Profit ($)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.axhline(0, color="red", linewidth=0.8, linestyle="--", alpha=0.6)

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "sales_vs_profit.png")
    plt.savefig(path)
    plt.close()
    print(f"   ✅ Saved: sales_vs_profit.png")


# ── 6. Bar Chart — Profit by Segment ────────────────────────────────────────
def plot_profit_by_segment(df):
    seg = df.groupby("Segment")["Profit"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(seg.index, seg.values, color=sns.color_palette("pastel", len(seg)))
    ax.set_title("Profit by Customer Segment", fontsize=14, fontweight="bold")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Total Profit ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 500,
                f"${bar.get_height():,.0f}",
                ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "profit_by_segment.png")
    plt.savefig(path)
    plt.close()
    print(f"   ✅ Saved: profit_by_segment.png")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_dataframe()
    df = clean_dataframe(df)

    print("\n📊 Generating charts...")
    plot_sales_by_region(df)
    plot_monthly_sales(df)
    plot_top_products(df)
    plot_heatmap(df)
    plot_sales_vs_profit(df)
    plot_profit_by_segment(df)

    print(f"\n✅ All charts saved to reports/")