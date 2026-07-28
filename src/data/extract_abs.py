from pathlib import Path

import pandas as pd


INPUT_FILE = Path(
    "data/raw/abs/crime_data.xlsx"
)

OUTPUT_FILE = Path(
    "data/raw/abs/table1_offenders.csv"
)


def extract_table_one():
    """
    Extract ABS Table 1 offender statistics.
    """

    df = pd.read_excel(
        INPUT_FILE,
        sheet_name="Table 1",
        header=5
    )

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


def save_table_one(df):
    """
    Save extracted table as CSV.
    """

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


if __name__ == "__main__":

    table = extract_table_one()

    print(table.head())

    save_table_one(table)

    print(
        f"Saved extracted table to {OUTPUT_FILE}"
    )