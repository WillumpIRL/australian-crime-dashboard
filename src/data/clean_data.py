import pandas as pd


COUNT_YEARS = [
    "2008–09",
    "2009–10",
    "2010–11",
    "2011–12",
    "2012–13",
    "2013–14",
    "2014–15",
    "2015–16",
    "2016–17",
    "2017–18",
    "2018–19",
    "2019–20",
    "2020–21",
    "2021–22",
    "2022–23",
    "2023–24",
    "2024–25",
]


RATE_YEARS = [
    f"{year}.1"
    for year in COUNT_YEARS
]


def clean_offender_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform ABS offender table into analytical format.
    """

    # Remove empty rows
    df = df.dropna(
        subset=["Principal offence(b)(c)"]
    )

    # Remove notes section
    df = df[
        ~df["Principal offence(b)(c)"]
        .astype(str)
        .str.startswith(("(", "©"))
    ]

    # Remove totals
    df = df[
        df["Principal offence(b)(c)"]
        != "Total(p)"
    ]

    # Rename offence column
    df = df.rename(
        columns={
            "Principal offence(b)(c)": 
            "Offence_Category"
        }
    )

    return df