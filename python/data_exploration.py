import pandas as pd
from pathlib import Path

# Path to raw data
DATA_PATH = Path("data/raw")

# Get all CSV files
csv_files = list(DATA_PATH.glob("*.csv"))

print("=" * 70)
print("RETAIL LOGISTICS DATA EXPLORATION")
print("=" * 70)

print(f"\nCSV files found: {len(csv_files)}")

for file in csv_files:

    print("\n" + "=" * 70)
    print(f"FILE: {file.name}")
    print("=" * 70)

    df = pd.read_csv(file)

    print(f"\nRows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumns:")
    print(list(df.columns))

    print(f"\nDuplicate rows: {df.duplicated().sum():,}")

    print("\nMissing values:")

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) == 0:
        print("No missing values")
    else:
        print(missing.sort_values(ascending=False))

    print("\nData types:")
    print(df.dtypes)

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

print("\n" + "=" * 70)
print("DATA EXPLORATION COMPLETED")
print("=" * 70)