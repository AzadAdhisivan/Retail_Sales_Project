"""
database.py
Part 3 - SQLite Integration:
  - Creates retail.db with normalized tables
  - Inserts all CSV data
  - Full CRUD operations
"""

import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "database", "retail.db")


# ── Connection ────────────────────────────────────────────────────────────────
def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


# ── CREATE — Build tables ─────────────────────────────────────────────────────
def create_tables(conn):
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id   TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            segment       TEXT,
            region        TEXT
        );

        CREATE TABLE IF NOT EXISTS Products (
            product_id    TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            category      TEXT,
            sub_category  TEXT
        );

        CREATE TABLE IF NOT EXISTS Orders (
            row_id        INTEGER PRIMARY KEY,
            order_id      TEXT NOT NULL,
            customer_id   TEXT NOT NULL,
            product_id    TEXT NOT NULL,
            order_date    TEXT,
            ship_date     TEXT,
            ship_mode     TEXT,
            sales         REAL,
            quantity      INTEGER,
            discount      REAL,
            profit        REAL,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (product_id)  REFERENCES Products(product_id)
        );
    """)

    conn.commit()
    print("   Tables created: Customers, Products, Orders")


# ── INSERT — Populate tables from CSV ─────────────────────────────────────────
def insert_data(conn, rows):
    cursor = conn.cursor()

    # Track unique customers and products to avoid duplicate inserts
    seen_customers = set()
    seen_products  = set()

    customers_data = []
    products_data  = []
    orders_data    = []

    for row in rows:
        # Customers
        cid = row["Customer ID"]
        if cid not in seen_customers:
            customers_data.append((
                cid,
                row["Customer Name"],
                row["Segment"],
                row["Region"]
            ))
            seen_customers.add(cid)

        # Products
        pid = row["Product ID"]
        if pid not in seen_products:
            products_data.append((
                pid,
                row["Product Name"],
                row["Category"],
                row["Sub-Category"]
            ))
            seen_products.add(pid)

        # Orders
        orders_data.append((
            int(row["Row ID"]),
            row["Order ID"],
            cid,
            pid,
            row["Order Date"],
            row["Ship Date"],
            row["Ship Mode"],
            float(row["Sales"]),
            int(row["Quantity"]),
            float(row["Discount"]),
            float(row["Profit"])
        ))

    cursor.executemany("INSERT OR IGNORE INTO Customers VALUES (?,?,?,?)", customers_data)
    cursor.executemany("INSERT OR IGNORE INTO Products  VALUES (?,?,?,?)", products_data)
    cursor.executemany("INSERT OR IGNORE INTO Orders    VALUES (?,?,?,?,?,?,?,?,?,?,?)", orders_data)

    conn.commit()
    print(f"   Inserted {len(customers_data)} customers")
    print(f"   Inserted {len(products_data)} products")
    print(f"   Inserted {len(orders_data)} orders")


# ── READ — Fetch records ──────────────────────────────────────────────────────
def read_sample(conn):
    cursor = conn.cursor()

    print("\n📖 Sample Customers (first 3):")
    for row in cursor.execute("SELECT * FROM Customers LIMIT 3"):
        print(f"   {row}")

    print("\n📖 Sample Products (first 3):")
    for row in cursor.execute("SELECT * FROM Products LIMIT 3"):
        print(f"   {row}")

    print("\n📖 Sample Orders (first 3):")
    for row in cursor.execute("SELECT * FROM Orders LIMIT 3"):
        print(f"   {row}")


# ── UPDATE — Update a customer region ─────────────────────────────────────────
def update_customer_region(conn, customer_id, new_region):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Customers SET region = ? WHERE customer_id = ?",
        (new_region, customer_id)
    )
    conn.commit()
    print(f"\n✏️  Updated customer {customer_id} region to '{new_region}'")


# ── DELETE — Delete an order by row_id ───────────────────────────────────────
def delete_order(conn, row_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Orders WHERE row_id = ?", (row_id,))
    conn.commit()
    print(f"\n🗑️  Deleted order with row_id = {row_id}")


# ── Table counts ──────────────────────────────────────────────────────────────
def print_counts(conn):
    cursor = conn.cursor()
    c = cursor.execute("SELECT COUNT(*) FROM Customers").fetchone()[0]
    p = cursor.execute("SELECT COUNT(*) FROM Products").fetchone()[0]
    o = cursor.execute("SELECT COUNT(*) FROM Orders").fetchone()[0]
    print(f"\n📊 Table counts:")
    print(f"   Customers : {c}")
    print(f"   Products  : {p}")
    print(f"   Orders    : {o}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    rows = load_csv()

    print("\n🗄️  Setting up database...")
    conn = get_connection()

    print("\n🔨 Creating tables...")
    create_tables(conn)

    print("\n📥 Inserting data...")
    insert_data(conn, rows)

    print_counts(conn)
    read_sample(conn)

    # Demo UPDATE
    update_customer_region(conn, "CG-12520", "West")

    # Demo DELETE
    delete_order(conn, 9994)

    print_counts(conn)

    conn.close()
    print(f"\n✅ Database saved to: {DB_PATH}")