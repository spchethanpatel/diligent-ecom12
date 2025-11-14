# ingest_to_sqlite.py
# Reads CSVs and loads them into a SQLite database (ecom.db)

import sqlite3
import pandas as pd
import os

DB_NAME = "ecom.db"

CSV_FILES = {
    "users": "users.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "reviews": "reviews.csv"
}

def load_csv_to_sqlite(csv_file, table_name, conn):
    """Reads a CSV file and loads into SQLite table."""
    df = pd.read_csv(csv_file)

    # Drop table if exists, then recreate it using pandas
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"✔ Loaded {table_name} ({len(df)} rows)")

def main():
    # Delete old database if exists
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("🗑 Removed old ecom.db")

    # Create new SQLite DB
    conn = sqlite3.connect(DB_NAME)
    print("📦 Created new ecom.db")

    # Load all CSV files
    for table, file in CSV_FILES.items():
        if not os.path.exists(file):
            print(f"⚠ CSV not found: {file}")
            continue
        load_csv_to_sqlite(file, table, conn)

    conn.close()
    print("\n✅ Data successfully loaded into ecom.db")

if __name__ == "__main__":
    main()
