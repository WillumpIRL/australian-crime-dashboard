import pandas as pd

from src.data.validate_data import validate_columns


def test_valid_columns():

    df = pd.DataFrame(
        {
            "Offence_Category": [
                "Homicide"
            ],
            "Year": [
                "2008–09"
            ],
            "Offender_Count": [
                816
            ],
            "Offender_Rate": [
                4.1
            ],
        }
    )

    assert validate_columns(df) is True