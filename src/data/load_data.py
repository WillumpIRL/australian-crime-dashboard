# Data loading functions
from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/raw/crime_data.csv")


def load_crime_data() -> pd.DataFrame:
    """
    Load raw crime data from CSV.

    Returns:
        pandas.DataFrame: Raw crime dataset.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    return pd.read_csv(DATA_PATH)