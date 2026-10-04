import pandas as pd
from pathlib import Path

CLEAN_PATH = Path("data/cleaned")
OUTPUT_PATH = Path("data/cleaned/logistics_analytics.csv")

print("=" * 70)
print("CREATING CENTRAL LOGISTICS ANALYTICS DATASET")
print("=" * 70)


# ---------------------------------------------------------
# 1. Load datasets
# ---------------------------------------------------------

print("\nLoading datasets...")

orders = pd.read_csv(
    CLEAN_PATH / "olist_orders_dataset.csv"
)

items = pd.read_csv(
    CLEAN_PATH / "olist_order_items_dataset.csv"
)

products = pd.read_csv(
    CLEAN_PATH / "olist_products_dataset.csv"
)

customers = pd.read_csv(
    CLEAN_PATH / "olist_customers_dataset.csv"
)

sellers = pd.read_csv(
    CLEAN_PATH / "olist_sellers_dataset.csv"
)

reviews = pd.read_csv(
    CLEAN_PATH / "olist_order_reviews_dataset.csv"
)

category_translation = pd.read_csv(
    CLEAN_PATH / "product_category_name_translation.csv"
)


# ---------------------------------------------------------
# 2. Convert dates
# ---------------------------------------------------------

date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:

    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )


# ---------------------------------------------------------
# 3. Calculate delivery metrics
# ---------------------------------------------------------

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / (60 * 60 * 24)


orders["delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / (60 * 60 * 24)


orders["delivery_status"] = orders["delay_days"].apply(
    lambda x:
        "Late"
        if x > 0
        else "On Time"
        if pd.notna(x)
        else "Unknown"
)


# ---------------------------------------------------------
# 4. Join orders with order items
# ---------------------------------------------------------

analytics = orders.merge(
    items,
    on="order_id",
    how="left"
)


# ---------------------------------------------------------
# 5. Join products
# ---------------------------------------------------------

analytics = analytics.merge(
    products,
    on="product_id",
    how="left"
)


# ---------------------------------------------------------
# 6. Join customers
# ---------------------------------------------------------

analytics = analytics.merge(
    customers,
    on="customer_id",
    how="left"
)


# ---------------------------------------------------------
# 7. Join sellers
# ---------------------------------------------------------

analytics = analytics.merge(
    sellers,
    on="seller_id",
    how="left"
)


# ---------------------------------------------------------
# 8. Join product category translation
# ---------------------------------------------------------

analytics = analytics.merge(
    category_translation,
    on="product_category_name",
    how="left"
)


# ---------------------------------------------------------
# 9. Join reviews
# ---------------------------------------------------------

reviews_small = reviews[
    [
        "order_id",
        "review_score"
    ]
].drop_duplicates("order_id")

analytics = analytics.merge(
    reviews_small,
    on="order_id",
    how="left"
)


# ---------------------------------------------------------
# 10. Select useful columns
# ---------------------------------------------------------

columns = [
    "order_id",
    "customer_id",
    "seller_id",
    "product_id",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "delivery_days",
    "delay_days",
    "delivery_status",
    "product_category_name_english",
    "price",
    "freight_value",
    "customer_city",
    "customer_state",
    "seller_city",
    "seller_state",
    "review_score"
]

# Keep only columns that exist
columns = [
    column for column in columns
    if column in analytics.columns
]

analytics = analytics[columns]


# ---------------------------------------------------------
# 11. Save dataset
# ---------------------------------------------------------

analytics.to_csv(
    OUTPUT_PATH,
    index=False
)


# ---------------------------------------------------------
# 12. Display summary
# ---------------------------------------------------------

print("\nAnalytics dataset created successfully!")

print(f"\nRows    : {len(analytics):,}")
print(f"Columns : {len(analytics.columns)}")

print("\nColumns:")
for column in analytics.columns:
    print(f"- {column}")

print("\nSample data:")
print(
    analytics.head(5).to_string(index=False)
)

print("\nSaved to:")
print(OUTPUT_PATH)

print("\n" + "=" * 70)
print("LOGISTICS ANALYTICS DATASET COMPLETED")
print("=" * 70)