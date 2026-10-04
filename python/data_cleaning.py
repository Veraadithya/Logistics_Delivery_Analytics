import pandas as pd
from pathlib import Path

# Paths
RAW_PATH = Path("data/raw")
CLEAN_PATH = Path("data/cleaned")

# Create cleaned-data folder if it doesn't exist
CLEAN_PATH.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("RETAIL LOGISTICS DATA CLEANING")
print("=" * 70)

# Get all CSV files
csv_files = list(RAW_PATH.glob("*.csv"))

for file in csv_files:

    print(f"\nProcessing: {file.name}")

    # Read CSV
    df = pd.read_csv(file)

    original_rows = len(df)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates > 0:
        df = df.drop_duplicates()

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Remove leading/trailing spaces from text columns
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].str.strip()

    # Save cleaned file
    output_file = CLEAN_PATH / file.name
    df.to_csv(output_file, index=False)

    print(f"Original rows : {original_rows:,}")
    print(f"Final rows    : {len(df):,}")
    print(f"Duplicates removed: {duplicates:,}")
    print(f"Saved to      : {output_file}")

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETED")
print("=" * 70)