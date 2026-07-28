# Data cleaning functions

import pandas as pd


COLUMN_MAPPING = {
    "Offence": "Offence_Category",
    "Count": "Crime_Count",
}


def clean_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise crime dataset columns.
    """

    df = df.rename(
        columns=COLUMN_MAPPING
    )

    df = df.drop_duplicates()

    return df