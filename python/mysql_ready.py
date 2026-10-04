import pandas as pd
from pathlib import Path

INPUT_FILE = Path("data/cleaned/logistics_analytics.csv")
OUTPUT_FILE = Path("data/cleaned/logistics_analytics_mysql.csv")

print("=" * 70)
print("CREATING MYSQL-READY CSV")
print("=" * 70)

df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False
)

print(f"Original rows: {len(df):,}")

# Remove whitespace and hidden newline characters
for column in df.columns:
    df[column] = (
        df[column]
        .astype(str)
        .str.replace("\r", "", regex=False)
        .str.replace("\n", "", regex=False)
        .str.strip()
    )

# Convert blank values to NULL-compatible empty fields
df = df.replace("", pd.NA)

# Numeric columns
numeric_columns = [
    "delivery_days",
    "delay_days",
    "price",
    "freight_value",
    "review_score"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# Date columns
date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        ).dt.strftime("%Y-%m-%d %H:%M:%S")

# Replace pandas NaN/NaT with empty strings for MySQL import
df = df.fillna("")

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8",
    lineterminator="\n"
)

print(f"Cleaned rows: {len(df):,}")
print(f"Output file: {OUTPUT_FILE}")

print("\nReview score values:")
print(df["review_score"].value_counts(dropna=False))

print("\n" + "=" * 70)
print("MYSQL-READY CSV CREATED")
print("=" * 70)