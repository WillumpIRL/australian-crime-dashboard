import pandas as pd

from src.data.clean_data import reshape_offender_counts


def test_wide_to_long():

    df = pd.DataFrame(
        {
            "Offence_Category": [
                "Homicide"
            ],
            "2008–09": [
                816
            ],
            "2009–10": [
                880
            ],
        }
    )

    result = reshape_offender_counts(df)

    assert len(result) == 2

    assert (
        result.iloc[0]["Year"]
        == "2008–09"
    )

    assert (
        result.iloc[0]["Offender_Count"]
        == 816
    )