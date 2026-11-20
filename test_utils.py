import pytest

from utils import load_csv_data, validate_columns


def test_load_and_validate(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text("t,T\n0,25\n1,26\n")
    df = load_csv_data(str(p))
    assert validate_columns(df, ["t", "T"]) is True
    with pytest.raises(ValueError):
        validate_columns(df, ["t", "dpd"])


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_csv_data(str(tmp_path / "nope.csv"))
