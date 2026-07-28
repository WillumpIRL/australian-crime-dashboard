import pytest
import pandas as pd

from src.data.clean_data import (
    clean_offender_data,
    create_final_dataset,
)
@pytest.fixture
def cleaned_data():

    data = {
        "Principal offence(b)(c)": [
            "011 Murder",
            "021 Assault",
            "(a) Notes section"
        ],
        "2008–09": [
            318,
            69218,
            None
        ],
        "2008–09.1": [
            1.7,
            369.0,
            None
        ],
    }

    raw = pd.DataFrame(data)

    return clean_offender_data(raw)

@pytest.fixture
def cleaned_dataset():

    years = [
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

    rows = []

    for year in years:
        rows.append(
            {
                "Offence_Category": "011 Murder",
                "Year": year,
                "Offender_Count": 300,
                "Offender_Rate": 1.5,
            }
        )

    return pd.DataFrame(rows)