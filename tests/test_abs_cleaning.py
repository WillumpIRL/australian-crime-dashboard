import pandas as pd

from src.data.clean_data import clean_offender_data


def test_remove_notes():

    df = pd.DataFrame(
        {
            "Principal offence(b)(c)": [
                "01 Homicide",
                None,
                "(a) Rate note",
                "Total(p)"
            ],
            "2008–09": [
                10,
                None,
                None,
                10
            ]
        }
    )

    cleaned = clean_offender_data(df)

    assert len(cleaned) == 1
    assert (
        cleaned.iloc[0]["Offence_Category"]
        == "01 Homicide"
    )