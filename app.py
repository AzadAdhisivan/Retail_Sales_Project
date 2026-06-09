"""
app.py
Streamlit UI for Retail Sales Analytics & Prediction System
"""

import sys
import os
import sqlite3
import pickle

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from data_loader import load_csv

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(__file__)
DB_PATH  = os.path.join(BASE_DIR, "database", "retail.db")

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 110


# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_dataframe():
    rows = load_csv()
    df   = pd.DataFrame(rows)
    df["Sales"]      = pd.to_numeric(df["Sales"])
    df["Profit"]     = pd.to_numeric(df["Profit"])
    df["Discount"]   = pd.to_numeric(df["Discount"])
    df["Quantity"]   = pd.to_numeric(df["Quantity"])
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Month Num"]  = df["Order Date"].dt.month
    df["Year"]       = df["Order Date"].dt.year
    return df


@st.cache_data
def get_ml_results():
    path = os.path.join(BASE_DIR, "reports", "ml_results.pkl")
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return pickle.load(f)


def get_db():
    return sqlite3.connect(DB_PATH)


# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🛒 Retail Sales")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "📊 EDA",
    "🏆 Products",
    "🗄️ SQL Reports",
    "🤖 ML Models"
])
st.sidebar.markdown("---")
st.sidebar.caption("Superstore Dataset · 9,994 orders")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.title("🛒 Retail Sales Analytics & Prediction")
    st.markdown("A complete data science pipeline — from raw CSV to ML predictions.")
    st.markdown("---")

    df = get_dataframe()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales",      f"${df['Sales'].sum():,.0f}")
    col2.metric("Total Profit",     f"${df['Profit'].sum():,.0f}")
    col3.metric("Unique Customers", f"{df['Customer ID'].nunique():,}")
    col4.metric("Unique Products",  f"{df['Product ID'].nunique():,}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dataset Overview")
        st.dataframe(df[[
            "Order ID", "Customer Name", "Category",
            "Region", "Sales", "Profit", "Discount"
        ]].head(10), use_container_width=True)

    with col2:
        st.subheader("Sales by Category")
        cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(cat.index, cat.values, color=sns.color_palette("muted", len(cat)))
        ax.set_ylabel("Sales ($)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        for i, (idx, val) in enumerate(cat.items()):
            ax.text(i, val + 5000, f"${val:,.0f}", ha="center", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("Project Structure")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Part 1 — Python Fundamentals**
        - CSV loader, data structures, OOP classes
        - Functional analysis, file handling

        **Part 2 — NumPy & Pandas**
        - Statistical analysis, EDA
        - Matplotlib & Seaborn visualizations
        """)
    with col2:
        st.markdown("""
        **Part 3 — SQL Integration**
        - SQLite database with 3 normalized tables
        - CRUD operations and analytical queries

        **Part 4 — Machine Learning**
        - Linear, Ridge, Lasso, Random Forest
        - MAE, RMSE, R2 evaluation
        """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — EDA
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 EDA":
    st.title("📊 Exploratory Data Analysis")
    df = get_dataframe()

    st.sidebar.markdown("### Filters")
    years    = sorted(df["Year"].unique())
    sel_year = st.sidebar.multiselect("Year", years, default=years)
    sel_reg  = st.sidebar.multiselect("Region", df["Region"].unique(), default=list(df["Region"].unique()))

    filtered = df[df["Year"].isin(sel_year) & df["Region"].isin(sel_reg)]

    st.markdown(f"Showing **{len(filtered):,}** orders")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sales by Region")
        region = filtered.groupby("Region")["Sales"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(region.index, region.values, color=sns.color_palette("muted", len(region)))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax.set_ylabel("Sales ($)")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Profit by Segment")
        seg = filtered.groupby("Segment")["Profit"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(seg.index, seg.values, color=sns.color_palette("pastel", len(seg)))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax.set_ylabel("Profit ($)")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.subheader("Monthly Sales Trend")
    monthly = filtered.groupby(["Month Num", "Month Name"])["Sales"].sum().reset_index().sort_values("Month Num")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(monthly["Month Name"], monthly["Sales"], marker="o", linewidth=2, color="#4C72B0")
    ax.fill_between(monthly["Month Name"], monthly["Sales"], alpha=0.15, color="#4C72B0")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.set_ylabel("Sales ($)")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("Profit Heatmap — Category x Region")
    pivot = filtered.pivot_table(values="Profit", index="Category", columns="Region", aggfunc="sum").round(0)
    fig, ax = plt.subplots(figsize=(8, 3))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("Sales vs Profit (colored by Discount)")
    fig, ax = plt.subplots(figsize=(10, 5))
    sc = ax.scatter(filtered["Sales"], filtered["Profit"],
                    c=filtered["Discount"], cmap="coolwarm", alpha=0.4, s=12)
    plt.colorbar(sc, ax=ax, label="Discount")
    ax.axhline(0, color="red", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Sales ($)")
    ax.set_ylabel("Profit ($)")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — PRODUCTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Products":
    st.title("🏆 Product Analysis")
    df = get_dataframe()

    top_n = st.slider("Show top N products", 5, 20, 10)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Top {top_n} by Sales")
        top_sales = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=True).tail(top_n)
        labels = [n[:35] for n in top_sales.index]
        fig, ax = plt.subplots(figsize=(7, top_n * 0.45 + 1))
        ax.barh(labels, top_sales.values, color=sns.color_palette("Blues_d", top_n))
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader(f"Top {top_n} by Profit")
        top_profit = df.groupby("Product Name")["Profit"].sum().sort_values(ascending=True).tail(top_n)
        labels = [n[:35] for n in top_profit.index]
        fig, ax = plt.subplots(figsize=(7, top_n * 0.45 + 1))
        ax.barh(labels, top_profit.values, color=sns.color_palette("Greens_d", top_n))
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("Profit Margin by Sub-Category")
    sub = df.groupby("Sub-Category").agg(
        Profit=("Profit", "sum"),
        Sales=("Sales", "sum")
    ).reset_index()
    sub["Margin %"] = (sub["Profit"] / sub["Sales"] * 100).round(2)
    sub = sub.sort_values("Margin %", ascending=False)
    st.dataframe(sub.style.background_gradient(subset=["Margin %"], cmap="RdYlGn"),
                 use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — SQL REPORTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗄️ SQL Reports":
    st.title("🗄️ SQL Reports")

    if not os.path.exists(DB_PATH):
        st.error("Database not found. Run python src/database.py first.")
        st.stop()

    conn = get_db()
    st.markdown("---")

    st.subheader("Revenue by Region")
    region_df = pd.read_sql("""
        SELECT c.region,
               ROUND(SUM(o.sales), 2)  AS total_sales,
               ROUND(SUM(o.profit), 2) AS total_profit,
               COUNT(o.row_id)         AS total_orders
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        GROUP BY c.region
        ORDER BY total_sales DESC
    """, conn)
    st.dataframe(region_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Profit by Category & Sub-Category")
    cat_df = pd.read_sql("""
        SELECT p.category, p.sub_category,
               ROUND(SUM(o.profit), 2) AS total_profit,
               ROUND(SUM(o.profit) / SUM(o.sales) * 100, 2) AS margin_pct
        FROM Orders o
        JOIN Products p ON o.product_id = p.product_id
        GROUP BY p.category, p.sub_category
        ORDER BY total_profit DESC
    """, conn)
    st.dataframe(cat_df.style.background_gradient(subset=["total_profit"], cmap="RdYlGn"),
                 use_container_width=True)

    st.markdown("---")
    st.subheader("Top Loss-Making Orders")
    loss_df = pd.read_sql("""
        SELECT o.order_id, c.name AS customer, p.category,
               ROUND(o.sales, 2) AS sales,
               ROUND(o.profit, 2) AS profit,
               o.discount
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        JOIN Products  p ON o.product_id  = p.product_id
        WHERE o.profit < 0
        ORDER BY o.profit ASC
        LIMIT 20
    """, conn)
    st.dataframe(loss_df.style.background_gradient(subset=["profit"], cmap="Reds_r"),
                 use_container_width=True)

    conn.close()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — ML MODELS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 ML Models":
    st.title("🤖 Machine Learning — Sales Prediction")

    data = get_ml_results()
    if data is None:
        st.error("ML results not found. Run python src/ml_model.py first.")
        st.stop()

    results     = data["results"]
    y_test      = data["y_test"]
    importances = data["importances"]

    st.subheader("Model Comparison")
    summary = pd.DataFrame([
        {"Model": r["model"], "MAE": round(r["MAE"], 2),
         "RMSE": round(r["RMSE"], 2), "R2": round(r["R2"], 4)}
        for r in results
    ])
    best = summary.loc[summary["R2"].idxmax(), "Model"]
    st.dataframe(summary.style.highlight_max(subset=["R2"], color="#c6efce")
                              .highlight_min(subset=["MAE", "RMSE"], color="#c6efce"),
                 use_container_width=True)
    st.success(f"Best model: {best}")

    st.markdown("---")
    st.subheader("Actual vs Predicted Sales")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    for i, r in enumerate(results):
        ax = axes[i]
        ax.scatter(y_test, r["y_pred"], alpha=0.3, s=8, color="#4C72B0")
        mn = min(float(y_test.min()), float(r["y_pred"].min()))
        mx = max(float(y_test.max()), float(r["y_pred"].max()))
        ax.plot([mn, mx], [mn, mx], "r--", linewidth=1.5)
        ax.set_title(f"{r['model']}\nR2 = {r['R2']:.4f}", fontweight="bold", fontsize=10)
        ax.set_xlabel("Actual ($)")
        ax.set_ylabel("Predicted ($)")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    st.subheader("Feature Importance — Random Forest")
    sorted_imp = sorted(importances.items(), key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh([i[0] for i in sorted_imp], [i[1] for i in sorted_imp],
            color=sns.color_palette("Blues_d", len(sorted_imp)))
    ax.set_xlabel("Importance Score")
    for i, (feat, val) in enumerate(sorted_imp):
        ax.text(val + 0.002, i, f"{val:.4f}", va="center", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()