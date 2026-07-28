# Data validation functions
import pandas as pd


REQUIRED_COLUMNS = [
    "State",
    "Year",
    "Offence",
    "Count",
]


def validate_columns(df: pd.DataFrame) -> bool:
    """
    Check required dataset columns exist.
    """

    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return True