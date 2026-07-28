from pathlib import Path

import pandas as pd


INPUT_FILE = Path(
    "data/raw/abs/crime_data.xlsx"
)


def list_excel_sheets():
    """
    Display available worksheets.
    """

    workbook = pd.ExcelFile(INPUT_FILE)

    return workbook.sheet_names


if __name__ == "__main__":
    sheets = list_excel_sheets()

    for sheet in sheets:
        print(sheet)