import io
import pandas as pd
import pytest
from preprocessing import validate_and_preprocess, KDD_COLUMNS, CATEGORICAL_COLUMNS


def make_csv_stream(rows):
    df = pd.DataFrame(rows)
    csv_text = df.to_csv(index=False, header=False)
    return io.StringIO(csv_text)


def make_valid_row():
    row = [0] * 41
    row[1] = "tcp"
    row[2] = "http"
    row[3] = "SF"
    return row


def test_valid_csv_preprocesses_successfully():
    stream = make_csv_stream([make_valid_row()])
    df, row_count = validate_and_preprocess(stream, "test.csv")
    assert row_count == 1
    assert df.shape[0] == 1
    assert df.shape[1] == 41


def test_too_few_columns_is_rejected():
    stream = make_csv_stream([[0, 1, 2, 3, 4]])
    with pytest.raises(ValueError):
        validate_and_preprocess(stream, "test.csv")


def test_empty_file_is_rejected():
    stream = io.StringIO("")
    with pytest.raises(ValueError):
        validate_and_preprocess(stream, "empty.csv")


def test_unparseable_content_is_rejected():
    stream = io.StringIO("this is not valid csv data at all !!! \x00\x01")
    with pytest.raises(ValueError):
        validate_and_preprocess(stream, "garbage.csv")


def test_categorical_columns_get_encoded_to_numeric():
    stream = make_csv_stream([make_valid_row()])
    df, _ = validate_and_preprocess(stream, "test.csv")
    for col in CATEGORICAL_COLUMNS:
        assert pd.api.types.is_numeric_dtype(df[col])


def test_accepts_41_42_or_43_columns():
    row_43 = make_valid_row() + ["normal", 15]
    stream = make_csv_stream([row_43])
    df, row_count = validate_and_preprocess(stream, "test.csv")
    assert df.shape[1] == 41
    assert row_count == 1