"""
queries.py
Part 3 - SQL queries:
  - Monthly revenue growth
  - Highest profit categories
  - Orders incurring losses
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "database", "retail.db")


def get_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}\n"
            "Run database.py first to create it."
        )
    return sqlite3.connect(DB_PATH)


# ── 1. Monthly Revenue Growth ─────────────────────────────────────────────────
def monthly_revenue_growth(conn):
    cursor = conn.cursor()

    cursor.execute("""
        WITH monthly AS (
            SELECT
                STRFTIME('%Y-%m', SUBSTR(order_date, -4) || '-' ||
                    PRINTF('%02d', CAST(SUBSTR(order_date, 1, INSTR(order_date,'/')-1) AS INTEGER)) || '-' ||
                    PRINTF('%02d', CAST(SUBSTR(order_date, INSTR(order_date,'/')+1,
                        INSTR(SUBSTR(order_date, INSTR(order_date,'/')+1),'/')-1) AS INTEGER))
                ) AS month,
                SUM(sales) AS total_sales
            FROM Orders
            GROUP BY month
        )
        SELECT
            month,
            ROUND(total_sales, 2),
            ROUND(
                (total_sales - LAG(total_sales) OVER (ORDER BY month))
                / LAG(total_sales) OVER (ORDER BY month) * 100
            , 2) AS growth_pct
        FROM monthly
        ORDER BY month
    """)

    rows = cursor.fetchall()
    print("\n📅 Monthly Revenue Growth:")
    print(f"   {'Month':<10} {'Sales':>12} {'Growth %':>10}")
    print(f"   {'-'*10} {'-'*12} {'-'*10}")
    for month, sales, growth in rows:
        growth_str = f"{growth:>+.1f}%" if growth is not None else "   N/A"
        print(f"   {month:<10} ${sales:>11,.2f} {growth_str:>10}")

    return rows


# ── 2. Highest Profit Categories ──────────────────────────────────────────────
def highest_profit_categories(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.category,
            p.sub_category,
            ROUND(SUM(o.profit), 2)   AS total_profit,
            ROUND(SUM(o.sales), 2)    AS total_sales,
            ROUND(SUM(o.profit) / SUM(o.sales) * 100, 2) AS profit_margin_pct
        FROM Orders o
        JOIN Products p ON o.product_id = p.product_id
        GROUP BY p.category, p.sub_category
        ORDER BY total_profit DESC
    """)

    rows = cursor.fetchall()
    print("\n🏆 Profit by Category & Sub-Category:")
    print(f"   {'Category':<20} {'Sub-Category':<20} {'Profit':>10} {'Margin %':>10}")
    print(f"   {'-'*20} {'-'*20} {'-'*10} {'-'*10}")
    for cat, sub, profit, sales, margin in rows:
        print(f"   {cat:<20} {sub:<20} ${profit:>9,.2f} {margin:>9.1f}%")

    return rows


# ── 3. Orders Incurring Losses ────────────────────────────────────────────────
def loss_orders(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            o.order_id,
            c.name              AS customer,
            p.name              AS product,
            p.category,
            ROUND(o.sales, 2)   AS sales,
            ROUND(o.profit, 2)  AS profit,
            o.discount
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        JOIN Products  p ON o.product_id  = p.product_id
        WHERE o.profit < 0
        ORDER BY o.profit ASC
        LIMIT 15
    """)

    rows = cursor.fetchall()
    print(f"\n⚠️  Top 15 Loss-Making Orders:")
    print(f"   {'Order ID':<18} {'Customer':<20} {'Category':<15} {'Sales':>8} {'Profit':>9} {'Disc':>5}")
    print(f"   {'-'*18} {'-'*20} {'-'*15} {'-'*8} {'-'*9} {'-'*5}")
    for order_id, customer, product, category, sales, profit, discount in rows:
        print(f"   {order_id:<18} {customer:<20} {category:<15} ${sales:>7,.0f} ${profit:>8,.0f} {discount*100:>4.0f}%")

    return rows


# ── 4. Bonus — Revenue by Region ─────────────────────────────────────────────
def revenue_by_region(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.region,
            ROUND(SUM(o.sales), 2)  AS total_sales,
            ROUND(SUM(o.profit), 2) AS total_profit,
            COUNT(o.row_id)         AS total_orders
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        GROUP BY c.region
        ORDER BY total_sales DESC
    """)

    rows = cursor.fetchall()
    print(f"\n🌍 Revenue by Region:")
    print(f"   {'Region':<10} {'Sales':>12} {'Profit':>10} {'Orders':>8}")
    print(f"   {'-'*10} {'-'*12} {'-'*10} {'-'*8}")
    for region, sales, profit, orders in rows:
        print(f"   {region:<10} ${sales:>11,.2f} ${profit:>9,.2f} {orders:>8}")

    return rows


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    conn = get_connection()

    monthly_revenue_growth(conn)
    highest_profit_categories(conn)
    loss_orders(conn)
    revenue_by_region(conn)

    conn.close()
    print("\n✅ All queries complete.")