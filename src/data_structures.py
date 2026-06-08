"""
data_structures.py
Maps raw CSV rows into Python core data structures:
Lists, Dictionaries, Tuples, Sets.
"""

from data_loader import load_csv


def build_structures(rows):

    # ── LIST ──────────────────────────────────────────────────────────────────
    # All orders as a list of tuples (Order ID, Customer Name, Product Name, Sales, Profit)
    # Tuples are used here because each order snapshot shouldn't be changed
    orders_list = []
    for row in rows:
        order = (
            row["Order ID"],
            row["Customer Name"],
            row["Product Name"],
            float(row["Sales"]),
            float(row["Profit"])
        )
        orders_list.append(order)

    # ── DICTIONARY ────────────────────────────────────────────────────────────
    # Customer ID → Customer details
    customers_dict = {}
    for row in rows:
        cust_id = row["Customer ID"]
        if cust_id not in customers_dict:
            customers_dict[cust_id] = {
                "name":    row["Customer Name"],
                "segment": row["Segment"],
                "region":  row["Region"]
            }

    # Product ID → Product details
    products_dict = {}
    for row in rows:
        prod_id = row["Product ID"]
        if prod_id not in products_dict:
            products_dict[prod_id] = {
                "name":         row["Product Name"],
                "category":     row["Category"],
                "sub_category": row["Sub-Category"]
            }

    # ── SET ───────────────────────────────────────────────────────────────────
    # Unique values — sets automatically remove duplicates
    unique_regions     = set(row["Region"]   for row in rows)
    unique_categories  = set(row["Category"] for row in rows)
    unique_segments    = set(row["Segment"]  for row in rows)

    return orders_list, customers_dict, products_dict, unique_regions, unique_categories, unique_segments


if __name__ == "__main__":
    rows = load_csv()

    orders_list, customers_dict, products_dict, unique_regions, unique_categories, unique_segments = build_structures(rows)

    print(f"\n📋 LIST — Total orders tracked     : {len(orders_list)}")
    print(f"   Sample order (tuple)           : {orders_list[0]}")

    print(f"\n📖 DICT — Unique customers         : {len(customers_dict)}")
    print(f"   Sample customer                : {list(customers_dict.items())[0]}")

    print(f"\n📦 DICT — Unique products          : {len(products_dict)}")
    print(f"   Sample product                 : {list(products_dict.items())[0]}")

    print(f"\n🌍 SET  — Regions                  : {unique_regions}")
    print(f"🛒 SET  — Categories               : {unique_categories}")
    print(f"👤 SET  — Segments                 : {unique_segments}")