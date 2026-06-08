"""
models.py
OOP class structure for the Retail Sales project.
Classes: Customer, Product, Order, SalesAnalytics
"""

from data_loader import load_csv


# ── Customer ──────────────────────────────────────────────────────────────────
class Customer:
    def __init__(self, customer_id, name, segment, region):
        self.customer_id = customer_id
        self.name        = name
        self.segment     = segment
        self.region      = region

    def __repr__(self):
        return f"Customer({self.name}, {self.segment}, {self.region})"


# ── Product ───────────────────────────────────────────────────────────────────
class Product:
    def __init__(self, product_id, name, category, sub_category):
        self.product_id   = product_id
        self.name         = name
        self.category     = category
        self.sub_category = sub_category

    def __repr__(self):
        return f"Product({self.name}, {self.category})"


# ── Order ─────────────────────────────────────────────────────────────────────
class Order:
    def __init__(self, order_id, order_date, ship_date, ship_mode,
                 sales, quantity, discount, profit,
                 customer, product):
        self.order_id   = order_id
        self.order_date = order_date
        self.ship_date  = ship_date
        self.ship_mode  = ship_mode
        self.sales      = float(sales)
        self.quantity   = int(quantity)
        self.discount   = float(discount)
        self.profit     = float(profit)
        self.customer   = customer   # Customer object
        self.product    = product    # Product object

    def __repr__(self):
        return f"Order({self.order_id}, {self.customer.name}, ${self.sales})"


# ── SalesAnalytics ────────────────────────────────────────────────────────────
class SalesAnalytics:
    def __init__(self, orders):
        self.orders = orders  # list of Order objects

    # Total aggregate sales
    def total_sales(self):
        return round(sum(o.sales for o in self.orders), 2)

    # Top selling products
    def top_selling_products(self, top_n=10):
        product_sales = {}
        for o in self.orders:
            name = o.product.name
            product_sales[name] = product_sales.get(name, 0) + o.sales
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
        return sorted_products[:top_n]

    # High value customers
    def high_value_customers(self, top_n=10):
        customer_sales = {}
        for o in self.orders:
            name = o.customer.name
            customer_sales[name] = customer_sales.get(name, 0) + o.sales
        sorted_customers = sorted(customer_sales.items(), key=lambda x: x[1], reverse=True)
        return sorted_customers[:top_n]

    # Filter by region or category
    def filter_orders(self, region=None, category=None):
        filtered = []
        for o in self.orders:
            if region and o.customer.region.lower() != region.lower():
                continue
            if category and o.product.category.lower() != category.lower():
                continue
            filtered.append(o)
        return filtered

    # Detect duplicate order IDs
    def detect_duplicates(self):
        seen  = set()
        dupes = set()
        for o in self.orders:
            if o.order_id in seen:
                dupes.add(o.order_id)
            else:
                seen.add(o.order_id)
        return list(dupes)

    # Average discount
    def average_discount(self):
        return round(sum(o.discount for o in self.orders) / len(self.orders), 4)


# ── Builder — turns CSV rows into objects ─────────────────────────────────────
def build_objects(rows):
    """Takes raw CSV rows and returns a list of Order objects."""

    # Build unique Customer and Product objects first
    customers = {}
    products  = {}

    for row in rows:
        cid = row["Customer ID"]
        if cid not in customers:
            customers[cid] = Customer(
                customer_id = cid,
                name        = row["Customer Name"],
                segment     = row["Segment"],
                region      = row["Region"]
            )

        pid = row["Product ID"]
        if pid not in products:
            products[pid] = Product(
                product_id   = pid,
                name         = row["Product Name"],
                category     = row["Category"],
                sub_category = row["Sub-Category"]
            )

    # Build Order objects linking to Customer and Product
    orders = []
    for row in rows:
        order = Order(
            order_id   = row["Order ID"],
            order_date = row["Order Date"],
            ship_date  = row["Ship Date"],
            ship_mode  = row["Ship Mode"],
            sales      = row["Sales"],
            quantity   = row["Quantity"],
            discount   = row["Discount"],
            profit     = row["Profit"],
            customer   = customers[row["Customer ID"]],
            product    = products[row["Product ID"]]
        )
        orders.append(order)

    return orders


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    rows   = load_csv()
    orders = build_objects(rows)

    print(f"\n✅ Built {len(orders)} Order objects")
    print(f"   Sample Order   : {orders[0]}")
    print(f"   Its Customer   : {orders[0].customer}")
    print(f"   Its Product    : {orders[0].product}")

    analytics = SalesAnalytics(orders)

    print(f"\n💰 Total Sales: ${analytics.total_sales():,.2f}")

    print(f"\n🏆 Top 5 Products:")
    for i, (name, sales) in enumerate(analytics.top_selling_products(5), 1):
        print(f"   {i}. {name[:50]:<50} ${sales:,.2f}")

    print(f"\n👤 Top 5 Customers:")
    for i, (name, sales) in enumerate(analytics.high_value_customers(5), 1):
        print(f"   {i}. {name:<25} ${sales:,.2f}")

    print(f"\n🌍 West region orders  : {len(analytics.filter_orders(region='West'))}")
    print(f"🛒 Technology orders   : {len(analytics.filter_orders(category='Technology'))}")
    print(f"🔍 Duplicate Order IDs : {len(analytics.detect_duplicates())}")
    print(f"🏷️  Average Discount    : {analytics.average_discount() * 100:.2f}%")