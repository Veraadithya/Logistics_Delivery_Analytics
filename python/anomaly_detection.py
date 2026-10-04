import pandas as pd
from pathlib import Path

CLEAN_PATH = Path("data/cleaned")

print("=" * 70)
print("RETAIL LOGISTICS ANOMALY DETECTION")
print("=" * 70)


# Load orders
orders_file = CLEAN_PATH / "olist_orders_dataset.csv"

orders = pd.read_csv(orders_file)


# Convert dates
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )


# ---------------------------------------------------------
# 1. Calculate delivery time
# ---------------------------------------------------------

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / (60 * 60 * 24)


# ---------------------------------------------------------
# 2. Calculate delay
# ---------------------------------------------------------

orders["delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / (60 * 60 * 24)


# ---------------------------------------------------------
# 3. Delivery status
# ---------------------------------------------------------

orders["delivery_status"] = orders["delay_days"].apply(
    lambda x:
        "Late" if x > 0
        else "On Time"
        if pd.notna(x)
        else "Unknown"
)


# ---------------------------------------------------------
# 4. Find impossible delivery records
# ---------------------------------------------------------

invalid_delivery = orders[
    orders["delivery_days"] < 0
]

print("\n" + "-" * 70)
print("1. IMPOSSIBLE DELIVERY RECORDS")
print("-" * 70)

print(f"Records found: {len(invalid_delivery):,}")


# ---------------------------------------------------------
# 5. Find very long deliveries
# ---------------------------------------------------------

long_deliveries = orders[
    orders["delivery_days"] > 60
]

print("\n" + "-" * 70)
print("2. VERY LONG DELIVERIES")
print("-" * 70)

print(f"Deliveries over 60 days: {len(long_deliveries):,}")


# ---------------------------------------------------------
# 6. Find late deliveries
# ---------------------------------------------------------

late_deliveries = orders[
    orders["delivery_status"] == "Late"
]

print("\n" + "-" * 70)
print("3. LATE DELIVERIES")
print("-" * 70)

print(f"Late deliveries: {len(late_deliveries):,}")


# ---------------------------------------------------------
# 7. Find extremely late deliveries
# ---------------------------------------------------------

extreme_delays = orders[
    orders["delay_days"] > 30
]

print("\n" + "-" * 70)
print("4. EXTREME DELIVERY DELAYS")
print("-" * 70)

print(f"Orders delayed over 30 days: {len(extreme_delays):,}")


# ---------------------------------------------------------
# 8. Show examples
# ---------------------------------------------------------

print("\n" + "-" * 70)
print("EXAMPLE ANOMALIES")
print("-" * 70)

if len(extreme_delays) > 0:

    print(
        extreme_delays[
            [
                "order_id",
                "order_purchase_timestamp",
                "order_estimated_delivery_date",
                "order_delivered_customer_date",
                "delay_days"
            ]
        ].head(10).to_string(index=False)
    )

else:

    print("No extreme delays found.")


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

output_file = Path("reports/anomaly_report.csv")

orders.to_csv(output_file, index=False)

print("\n" + "=" * 70)
print("ANOMALY DETECTION COMPLETED")
print("=" * 70)

print(f"\nReport saved to: {output_file}")