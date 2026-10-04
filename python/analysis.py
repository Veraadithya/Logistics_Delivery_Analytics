import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

DATA_PATH = Path("data/cleaned")
OUTPUT_PATH = Path("data/cleaned/logistics_analytics.csv")

print("=" * 70)
print("RETAIL LOGISTICS ANALYSIS")
print("=" * 70)


# ---------------------------------------------------------
# 1. Load datasets
# ---------------------------------------------------------

print("\nLoading datasets...")

orders = pd.read_csv(DATA_PATH / "olist_orders_dataset.csv")
items = pd.read_csv(DATA_PATH / "olist_order_items_dataset.csv")
products = pd.read_csv(DATA_PATH / "olist_products_dataset.csv")
customers = pd.read_csv(DATA_PATH / "olist_customers_dataset.csv")
sellers = pd.read_csv(DATA_PATH / "olist_sellers_dataset.csv")
reviews = pd.read_csv(DATA_PATH / "olist_order_reviews_dataset.csv")
translation = pd.read_csv(
    DATA_PATH / "product_category_name_translation.csv"
)

print("All datasets loaded successfully.")


# ---------------------------------------------------------
# 2. Convert order dates
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
# 3. Calculate delivery days
# ---------------------------------------------------------

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / (60 * 60 * 24)


# ---------------------------------------------------------
# 4. Calculate delay days
# ---------------------------------------------------------

orders["delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / (60 * 60 * 24)


# ---------------------------------------------------------
# 5. Create delivery status
# ---------------------------------------------------------

orders["delivery_status"] = orders["delay_days"].apply(
    lambda x:
        "Late"
        if x > 0
        else "On Time"
        if pd.notna(x)
        else "Unknown"
)


# ---------------------------------------------------------
# 6. Join Orders + Items
# ---------------------------------------------------------

analysis = orders.merge(
    items,
    on="order_id",
    how="left"
)


# ---------------------------------------------------------
# 7. Join Products
# ---------------------------------------------------------

analysis = analysis.merge(
    products,
    on="product_id",
    how="left"
)


# ---------------------------------------------------------
# 8. Join Customers
# ---------------------------------------------------------

analysis = analysis.merge(
    customers,
    on="customer_id",
    how="left"
)


# ---------------------------------------------------------
# 9. Join Sellers
# ---------------------------------------------------------

analysis = analysis.merge(
    sellers,
    on="seller_id",
    how="left"
)


# ---------------------------------------------------------
# 10. Translate product categories
# ---------------------------------------------------------

analysis = analysis.merge(
    translation,
    on="product_category_name",
    how="left"
)


# ---------------------------------------------------------
# 11. Add review score
# ---------------------------------------------------------

review_data = reviews[
    ["order_id", "review_score"]
].drop_duplicates("order_id")

analysis = analysis.merge(
    review_data,
    on="order_id",
    how="left"
)


# ---------------------------------------------------------
# 12. Select important columns
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

analysis = analysis[
    [column for column in columns if column in analysis.columns]
]


# ---------------------------------------------------------
# 13. Save central dataset
# ---------------------------------------------------------

analysis.to_csv(
    OUTPUT_PATH,
    index=False
)


# ---------------------------------------------------------
# 14. Display summary
# ---------------------------------------------------------

print("\n" + "-" * 70)
print("ANALYSIS DATASET SUMMARY")
print("-" * 70)

print(f"Rows    : {len(analysis):,}")
print(f"Columns : {len(analysis.columns)}")

print("\nImportant metrics:")

print(
    f"Average delivery days: "
    f"{analysis['delivery_days'].mean():.2f}"
)

print(
    f"Average delay days: "
    f"{analysis['delay_days'].mean():.2f}"
)

late_orders = (
    analysis["delivery_status"] == "Late"
).sum()

print(f"Late records: {late_orders:,}")

print("\nDelivery status:")
print(
    analysis["delivery_status"]
    .value_counts(dropna=False)
)

print("\nTop product categories:")

if "product_category_name_english" in analysis.columns:
    print(
        analysis["product_category_name_english"]
        .value_counts()
        .head(10)
    )

print("\nSaved to:")
print(OUTPUT_PATH)

print("\n" + "=" * 70)
print("ANALYSIS COMPLETED")
print("=" * 70)