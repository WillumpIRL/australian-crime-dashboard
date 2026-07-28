from pathlib import Path

import pandas as pd

from src.data.extract_abs import extract_table_one
from src.data.clean_data import (
    clean_offender_data,
    create_final_dataset,
)
from src.data.validate_data import validate_columns


OUTPUT_FILE = Path(
    "data/processed/offenders_clean.csv"
)


def build_dataset():
    """
    Execute complete ABS offender ETL pipeline.
    """
    
    print("Extracting ABS data...")

    raw = extract_table_one()

    print("Cleaning data...")

    cleaned = clean_offender_data(raw)


    print("Reshaping dataset...")

    final = create_final_dataset(
        cleaned
    )


    print("Validating data...")

    validate_columns(
        final
    )


    print("Saving dataset...")

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    final.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print(
        f"Dataset saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    build_dataset()