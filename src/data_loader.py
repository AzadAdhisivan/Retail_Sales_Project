"""
data_loader.py
Loads the Superstore CSV using standard Python libraries only.
"""

import csv
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "Sample - Superstore.csv")


def load_csv(path=DATA_PATH):
    """Load the Superstore CSV and return a list of row dictionaries."""

    # Check file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Check not empty
    if not rows:
        raise ValueError("The CSV file is empty.")

    print(f"✅ Loaded {len(rows)} rows from '{os.path.basename(path)}'")
    print(f"   Columns: {list(rows[0].keys())}")

    return rows


if __name__ == "__main__":
    data = load_csv()