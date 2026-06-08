"""
numpy_analysis.py
Part 2 - NumPy Tasks:
  - Convert Sales, Profit, Quantity to NumPy arrays
  - Statistical analysis
  - Array slicing, reshaping, normalization
"""

import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))
from data_loader import load_csv


# ── 1. Load & Convert to NumPy Arrays ────────────────────────────────────────
def get_arrays(rows):
    sales    = np.array([float(row["Sales"])    for row in rows])
    profit   = np.array([float(row["Profit"])   for row in rows])
    quantity = np.array([int(row["Quantity"])   for row in rows])
    return sales, profit, quantity


# ── 2. Statistical Analysis ───────────────────────────────────────────────────
def statistical_analysis(arr, name):
    print(f"\n📊 {name} Statistics:")
    print(f"   Mean     : {np.mean(arr):.2f}")
    print(f"   Median   : {np.median(arr):.2f}")
    print(f"   Std Dev  : {np.std(arr):.2f}")
    print(f"   Variance : {np.var(arr):.2f}")
    print(f"   Min      : {np.min(arr):.2f}")
    print(f"   Max      : {np.max(arr):.2f}")


# ── 3. Array Slicing ──────────────────────────────────────────────────────────
def array_slicing(sales):
    print("\n✂️  Array Slicing (Sales):")
    print(f"   First 5 values        : {sales[:5]}")
    print(f"   Last 5 values         : {sales[-5:]}")
    print(f"   Every 1000th value    : {sales[::1000]}")
    print(f"   Sales above $1000     : {sales[sales > 1000][:5]} ... ({len(sales[sales > 1000])} total)")


# ── 4. Reshaping ──────────────────────────────────────────────────────────────
def array_reshaping(sales):
    print("\n🔲 Array Reshaping (Sales):")

    # Take first 100 values and reshape into 10x10 grid
    sample = sales[:100]
    reshaped = sample.reshape(10, 10)
    print(f"   Original shape  : {sample.shape}")
    print(f"   Reshaped (10x10): {reshaped.shape}")
    print(f"   First row       : {reshaped[0].round(2)}")


# ── 5. Normalization ──────────────────────────────────────────────────────────
def normalize(arr):
    """Min-max normalization: scales all values between 0 and 1."""
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))


def normalization_demo(sales):
    normalized = normalize(sales)
    print("\n📐 Normalization (Sales → 0 to 1 scale):")
    print(f"   Original  range : ${np.min(sales):.2f}  to  ${np.max(sales):.2f}")
    print(f"   Normalized range: {np.min(normalized):.4f}  to  {np.max(normalized):.4f}")
    print(f"   First 5 normalized values: {normalized[:5].round(4)}")
    return normalized


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    rows = load_csv()

    print("\n🔢 Converting columns to NumPy arrays...")
    sales, profit, quantity = get_arrays(rows)
    print(f"   Sales array    : {sales.shape} | dtype: {sales.dtype}")
    print(f"   Profit array   : {profit.shape} | dtype: {profit.dtype}")
    print(f"   Quantity array : {quantity.shape} | dtype: {quantity.dtype}")

    statistical_analysis(sales,    "Sales")
    statistical_analysis(profit,   "Profit")
    statistical_analysis(quantity, "Quantity")

    array_slicing(sales)
    array_reshaping(sales)
    normalization_demo(sales)