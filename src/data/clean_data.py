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

def reshape_offender_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert ABS offender data from wide format
    into long analytical format.
    """

    offence_column = "Offence_Category"
    year_columns = [
        col for col in COUNT_YEARS if col in df.columns
    ]
    if not year_columns:
        raise ValueError(
            "No valid year columns found in dataset"
    )
    long_df = df.melt(
        id_vars=[offence_column],
        value_vars=year_columns,
        var_name="Year",
        value_name="Offender_Count"
    )

    return long_df

def reshape_offender_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert ABS offender rates into long format.
    """

    offence_column = "Offence_Category"
    rate_columns = [
        col for col in RATE_YEARS if col in df.columns
    ]
    if not rate_columns:
        raise ValueError(
            "No valid rate columns found in dataset"
        )

    rate_df = df.melt(
        id_vars=[offence_column],
        value_vars=rate_columns,
        var_name="Year",
        value_name="Offender_Rate"
    )

    rate_df["Year"] = (
        rate_df["Year"]
        .str.replace(".1", "", regex=False)
    )

    return rate_df

def create_final_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create final dashboard dataset.
    """

    counts = reshape_offender_counts(df)

    rates = reshape_offender_rates(df)

    final = counts.merge(
        rates,
        on=[
            "Offence_Category",
            "Year"
        ],
        how="left"
    )

    return final