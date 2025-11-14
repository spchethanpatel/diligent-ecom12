Diligent E-Commerce Demo

A complete mini data-engineering pipeline: data generation → ingestion → SQL analytics

This repository contains a fully working e-commerce simulation project built with Python and SQLite.
It demonstrates how raw synthetic data flows through an automated ETL-like process and becomes query-ready for analysis.

📦 Project Components
1️⃣ Synthetic Data Generator — generate_ecom_data.py

Creates realistic, randomized e-commerce datasets, including:

Users

Products

Orders

Order Items

Reviews (optional)

All files are saved automatically into a data/ directory.

2️⃣ SQLite Ingestion Script — ingest_to_sqlite.py

This script:

Creates the ecom.db SQLite database

Automatically builds all required tables

Loads each CSV into its corresponding table

Prints a confirmation summary for each dataset loaded

3️⃣ Analytical SQL Runner — run_query.py

Executes a real multi-table JOIN, combining:

users

orders

order_items

products

The output includes customer details, product details, pricing, quantity, and calculated line totals — exactly like a real e-commerce order report.

🚫 Auto-Ignored Files

Generated CSVs and the SQLite database are excluded using .gitignore to keep the repository clean and lightweight:

data/*.csv

ecom.db


