import pandas as pd

from src.data.validate_data import validate_columns


def test_valid_columns():

    df = pd.DataFrame(
        {
            "State": ["WA"],
            "Year": [2025],
            "Offence": ["Theft"],
            "Count": [100],
        }
    )

    assert validate_columns(df) is True