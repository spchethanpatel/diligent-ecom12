import sqlite3
import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

conn = sqlite3.connect("ecom.db")

query = """
SELECT 
    o.order_id,
    (u.first_name || ' ' || u.last_name) AS customer_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    oi.subtotal AS line_total,
    o.order_date
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LIMIT 50;
"""


df = pd.read_sql_query(query, conn)

print("\n📊 QUERY OUTPUT BELOW:\n")
print(df.to_string(index=False))   # <-- forces full table print

conn.close()
