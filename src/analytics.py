"""
analytics.py
Functional implementation for retail sales analysis.
"""

from data_loader import load_csv


# ── 1. Total Aggregate Sales ──────────────────────────────────────────────────
def calculate_total_sales(rows):
    total = sum(float(row["Sales"]) for row in rows)
    return round(total, 2)


# ── 2. Top Selling Products ───────────────────────────────────────────────────
def top_selling_products(rows, top_n=10):
    product_sales = {}

    for row in rows:
        name  = row["Product Name"]
        sales = float(row["Sales"])
        if name in product_sales:
            product_sales[name] += sales
        else:
            product_sales[name] = sales

    # Sort by sales descending and return top N
    sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
    return sorted_products[:top_n]


# ── 3. High Value Customers ───────────────────────────────────────────────────
def high_value_customers(rows, top_n=10):
    customer_sales = {}

    for row in rows:
        name  = row["Customer Name"]
        sales = float(row["Sales"])
        if name in customer_sales:
            customer_sales[name] += sales
        else:
            customer_sales[name] = sales

    sorted_customers = sorted(customer_sales.items(), key=lambda x: x[1], reverse=True)
    return sorted_customers[:top_n]


# ── 4. Filter Orders ──────────────────────────────────────────────────────────
def filter_orders(rows, region=None, category=None):
    filtered = []

    for row in rows:
        if region and row["Region"].lower() != region.lower():
            continue
        if category and row["Category"].lower() != category.lower():
            continue
        filtered.append(row)

    return filtered


# ── 5. Detect Duplicates ──────────────────────────────────────────────────────
def detect_duplicates(rows):
    seen     = set()
    dupes    = []

    for row in rows:
        order_id = row["Order ID"]
        if order_id in seen:
            dupes.append(order_id)
        else:
            seen.add(order_id)

    # Return unique duplicate IDs
    return list(set(dupes))


# ── 6. Average Discount ───────────────────────────────────────────────────────
def average_discount(rows):
    total    = sum(float(row["Discount"]) for row in rows)
    average  = total / len(rows)
    return round(average, 4)


# ── Run all ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    rows = load_csv()

    print("\n💰 Total Sales:")
    print(f"   ${calculate_total_sales(rows):,.2f}")

    print("\n🏆 Top 10 Selling Products:")
    for i, (product, sales) in enumerate(top_selling_products(rows), 1):
        print(f"   {i}. {product[:50]:<50} ${sales:,.2f}")

    print("\n👤 Top 10 High Value Customers:")
    for i, (customer, sales) in enumerate(high_value_customers(rows), 1):
        print(f"   {i}. {customer:<25} ${sales:,.2f}")

    print("\n🌍 Filter — Region: West")
    west_orders = filter_orders(rows, region="West")
    print(f"   {len(west_orders)} orders found in West")

    print("\n🛒 Filter — Category: Technology")
    tech_orders = filter_orders(rows, category="Technology")
    print(f"   {len(tech_orders)} orders found in Technology")

    print("\n🔍 Duplicate Order IDs detected:")
    dupes = detect_duplicates(rows)
    print(f"   {len(dupes)} duplicate Order IDs")
    print(f"   Sample: {dupes[:3]}")

    print("\n🏷️  Average Discount:")
    print(f"   {average_discount(rows) * 100:.2f}%")