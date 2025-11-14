# generate_ecom_data.py
# Generates 5 CSV files of synthetic e-commerce data:
# users.csv, products.csv, orders.csv, order_items.csv, reviews.csv

import random
from datetime import datetime, timedelta, UTC
import pandas as pd
from faker import Faker
import numpy as np

# ---- Config: change these counts if needed ----
N_USERS = 10000
N_PRODUCTS = 1000
N_ORDERS = 50000
N_ORDER_ITEMS = 120000
N_REVIEWS = 20000

# ---- Setup ----
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# FIX: utcnow() deprecated → use timezone-aware
now = datetime.now(UTC)

# ---- 1) USERS ----
users = []
tiers = ['Bronze','Silver','Gold','Platinum']
countries = ['United States','India','United Kingdom','Canada','Australia','Germany','France','Brazil','Japan','Netherlands']
genders = ['male','female','non-binary','prefer_not_to_say']

for i in range(1, N_USERS + 1):
    created_at = fake.date_time_between(start_date='-4y', end_date='now').replace(microsecond=0)
    users.append({
        'user_id': i,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': f'user{i}@{fake.free_email_domain()}',
        'gender': random.choice(genders),
        'country': random.choice(countries),
        'created_at': created_at.isoformat(sep='T'),
        'loyalty_tier': np.random.choice(tiers, p=[0.6,0.25,0.1,0.05])
    })

users_df = pd.DataFrame(users)
users_df.to_csv('users.csv', index=False)

# ---- 2) PRODUCTS ----
categories = ['Electronics','Clothing','Home','Beauty','Sports','Toys','Books','Garden','Automotive']
brands = ['Acme','Zenith','Orion','Nimbus','Vertex','Apex','Helix','Pioneer','Lumen','Solace']

products = []
for i in range(1, N_PRODUCTS + 1):
    created_at = fake.date_time_between(start_date='-5y', end_date='now').replace(microsecond=0)
    price = round(random.uniform(5.0, 2000.0), 2)
    products.append({
        'product_id': i,
        'sku': f'SKU-{100000 + i}',
        'name': fake.sentence(nb_words=3).rstrip('.'),
        'category': random.choice(categories),
        'price': price,
        'stock': random.randint(0, 1000),
        'brand': random.choice(brands),
        'created_at': created_at.isoformat(sep='T')
    })

products_df = pd.DataFrame(products)
products_df.to_csv('products.csv', index=False)

# ---- 3) ORDERS ----
orders = []
for order_id in range(1, N_ORDERS + 1):
    user_row = users_df.sample(1).iloc[0]
    user_created = datetime.fromisoformat(user_row['created_at'])

    delta_days = (now.replace(tzinfo=None) - user_created).days
    if delta_days <= 0:
        order_date = now
    else:
        order_date = user_created + timedelta(days=random.randint(0, delta_days))

    order_date = order_date.replace(
        hour=random.randint(0,23),
        minute=random.randint(0,59),
        second=random.randint(0,59)
    )

    orders.append({
        'order_id': order_id,
        'user_id': int(user_row['user_id']),
        'total_amount': 0.0,  # will be replaced later
        'order_date': order_date.isoformat(sep='T'),
        'shipping_address': fake.address().replace('\n',' , '),
        'payment_method': random.choice(['credit_card','debit_card','paypal','wallet','upi']),
        'order_status': np.random.choice(
            ['completed','shipped','processing','cancelled','returned'],
            p=[0.7,0.15,0.1,0.03,0.02]
        )
    })

orders_df = pd.DataFrame(orders)

# ---- 4) ORDER_ITEMS ----
order_items = []
product_ids = products_df['product_id'].tolist()

for oi_id in range(1, N_ORDER_ITEMS + 1):
    order_id = random.randint(1, N_ORDERS)
    product_id = random.choice(product_ids)
    product_row = products_df.loc[products_df['product_id'] == product_id].iloc[0]

    unit_price = float(product_row['price'])
    quantity = random.randint(1,5)
    discount_pct = random.choice([0,0,0,0.05,0.1,0.2])
    discount = round(discount_pct * unit_price * quantity, 2)
    subtotal = round(unit_price * quantity - discount, 2)

    order_items.append({
        'order_item_id': oi_id,
        'order_id': order_id,
        'product_id': product_id,
        'quantity': quantity,
        'unit_price': unit_price,
        'discount': discount,
        'subtotal': subtotal
    })

order_items_df = pd.DataFrame(order_items)

# ---- FIX: Recalculate totals correctly ----
totals = (
    order_items_df
    .groupby('order_id')['subtotal']
    .sum()
    .reset_index()
    .rename(columns={'subtotal': 'total_amount'})
)

orders_df = orders_df.drop(columns=['total_amount'])
orders_df = orders_df.merge(totals, on='order_id', how='left')
orders_df['total_amount'] = orders_df['total_amount'].fillna(0.0)

orders_df.to_csv('orders.csv', index=False)
order_items_df.to_csv('order_items.csv', index=False)

# ---- 5) REVIEWS ----
reviews = []
for i in range(1, N_REVIEWS + 1):
    product_id = random.choice(product_ids)
    user_id = random.randint(1, N_USERS)
    rating = random.randint(1,5)

    title = fake.sentence(nb_words=6).rstrip('.')
    body = fake.paragraph(nb_sentences=3)

    product_created = datetime.fromisoformat(
        products_df.loc[products_df['product_id']==product_id,'created_at'].iloc[0]
    )
    user_created = datetime.fromisoformat(
        users_df.loc[users_df['user_id']==user_id,'created_at'].iloc[0]
    )

    start_date = max(product_created, user_created)
    delta_days = max(0, (now.replace(tzinfo=None) - start_date).days)

    if delta_days == 0:
        review_date = now
    else:
        review_date = start_date + timedelta(days=random.randint(0, delta_days))

    review_date = review_date.replace(
        hour=random.randint(0,23),
        minute=random.randint(0,59),
        second=random.randint(0,59)
    )

    reviews.append({
        'review_id': i,
        'product_id': product_id,
        'user_id': user_id,
        'rating': rating,
        'title': title,
        'body': body,
        'review_date': review_date.isoformat(sep='T'),
        'helpful_votes': random.randint(0, 50)
    })

reviews_df = pd.DataFrame(reviews)
reviews_df.to_csv('reviews.csv', index=False)

print("Done — generated: users.csv, products.csv, orders.csv, order_items.csv, reviews.csv")
