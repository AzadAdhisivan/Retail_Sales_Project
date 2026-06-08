"""
file_handler.py
Exports a cleaned dataset and a JSON summary report.
"""

import csv
import json
import os
from data_loader import load_csv
from analytics import (
    calculate_total_sales,
    top_selling_products,
    high_value_customers,
    average_discount,
    detect_duplicates
)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_PATH = os.path.join(BASE_DIR, "data", "cleaned_superstore.csv")
REPORT_PATH  = os.path.join(BASE_DIR, "reports", "summary_report.json")


# ── Step 1: Clean the data ────────────────────────────────────────────────────
def clean_rows(rows):
    """
    Remove rows with:
    - Missing Order ID or Customer ID
    - Invalid Sales, Profit, Discount, or Quantity values
    """
    cleaned = []
    skipped = 0

    for row in rows:
        # Check critical fields exist
        if not row.get("Order ID") or not row.get("Customer ID"):
            skipped += 1
            continue

        # Check numeric fields are valid
        try:
            float(row["Sales"])
            float(row["Profit"])
            float(row["Discount"])
            int(row["Quantity"])
        except (ValueError, TypeError):
            skipped += 1
            continue

        cleaned.append(row)

    print(f"   Rows kept    : {len(cleaned)}")
    print(f"   Rows skipped : {skipped}")
    return cleaned


# ── Step 2: Export cleaned CSV ────────────────────────────────────────────────
def export_cleaned_csv(rows, path=CLEANED_PATH):
    """Save cleaned rows to a new CSV file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"   Saved to: {path}")

    except PermissionError:
        raise PermissionError(f"Cannot write to {path}. Check folder permissions.")
    except Exception as e:
        raise Exception(f"Failed to export CSV: {e}")


# ── Step 3: Export JSON summary report ───────────────────────────────────────
def export_json_report(rows, path=REPORT_PATH):
    """Generate and save a JSON summary report."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        report = {
            "total_rows"         : len(rows),
            "total_sales"        : calculate_total_sales(rows),
            "average_discount_pct": round(average_discount(rows) * 100, 2),
            "duplicate_order_ids": len(detect_duplicates(rows)),
            "top_10_products"    : [
                {"product": name, "sales": round(sales, 2)}
                for name, sales in top_selling_products(rows, 10)
            ],
            "top_10_customers"   : [
                {"customer": name, "sales": round(sales, 2)}
                for name, sales in high_value_customers(rows, 10)
            ]
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"   Saved to: {path}")

    except Exception as e:
        raise Exception(f"Failed to export JSON report: {e}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Load raw data
    rows = load_csv()

    # Clean
    print("\n🧹 Cleaning data...")
    cleaned = clean_rows(rows)

    # Export cleaned CSV
    print("\n💾 Exporting cleaned CSV...")
    export_cleaned_csv(cleaned)

    # Export JSON report
    print("\n📝 Exporting JSON summary report...")
    export_json_report(cleaned)

    print("\n✅ Done! Check your data/ and reports/ folders.")