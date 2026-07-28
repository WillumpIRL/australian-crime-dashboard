from src.data.extract_abs import extract_table_one


def test_column_names_are_clean():

    df = extract_table_one()

    for column in df.columns:
        assert column == column.strip()