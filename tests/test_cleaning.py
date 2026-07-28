import pandas as pd

from src.data.clean_data import clean_crime_data


def test_column_standardisation():

    raw = pd.DataFrame(
        {
            "Offence": ["Theft"],
            "Count": [50],
        }
    )

    cleaned = clean_crime_data(raw)

    assert "Offence_Category" in cleaned.columns
    assert "Crime_Count" in cleaned.columns