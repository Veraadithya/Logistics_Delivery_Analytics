import pandas as pd
from pathlib import Path

CLEAN_PATH = Path("data/cleaned")

print("=" * 70)
print("RETAIL LOGISTICS DATA QUALITY CHECK")
print("=" * 70)


# ---------------------------------------------------------
# 1. Check missing values
# ---------------------------------------------------------

def check_missing_values(df, file_name):

    print(f"\n[MISSING VALUES] {file_name}")

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("No missing values found.")
    else:
        print(missing.sort_values(ascending=False))


# ---------------------------------------------------------
# 2. Check duplicate rows
# ---------------------------------------------------------

def check_duplicates(df, file_name):

    duplicates = df.duplicated().sum()

    print(f"\n[DUPLICATES] {file_name}")
    print(f"Duplicate rows: {duplicates:,}")


# ---------------------------------------------------------
# 3. Check null IDs
# ---------------------------------------------------------

def check_id_columns(df, file_name):

    print(f"\n[ID CHECK] {file_name}")

    id_columns = [
        column for column in df.columns
        if column.endswith("_id")
    ]

    if not id_columns:
        print("No ID columns found.")
        return

    for column in id_columns:

        null_count = df[column].isnull().sum()

        print(
            f"{column}: "
            f"{null_count:,} missing"
        )


# ---------------------------------------------------------
# 4. Check date columns
# ---------------------------------------------------------

def check_dates(df, file_name):

    print(f"\n[DATE CHECK] {file_name}")

    date_columns = [
        column for column in df.columns
        if "date" in column or "timestamp" in column
    ]

    if not date_columns:
        print("No date columns found.")
        return

    for column in date_columns:

        dates = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        invalid_dates = dates.isnull().sum()

        print(
            f"{column}: "
            f"{invalid_dates:,} invalid/missing"
        )


# ---------------------------------------------------------
# Process all cleaned CSV files
# ---------------------------------------------------------

csv_files = list(CLEAN_PATH.glob("*.csv"))

print(f"\nCSV files found: {len(csv_files)}")

for file in csv_files:

    print("\n" + "-" * 70)
    print(f"FILE: {file.name}")
    print("-" * 70)

    df = pd.read_csv(file)

    check_missing_values(df, file.name)
    check_duplicates(df, file.name)
    check_id_columns(df, file.name)
    check_dates(df, file.name)


print("\n" + "=" * 70)
print("DATA QUALITY CHECK COMPLETED")
print("=" * 70)