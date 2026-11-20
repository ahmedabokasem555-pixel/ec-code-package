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


import numpy as np
import pandas as pd

from utils import charge_at, charge_from_df, undiluted_concentration


def test_charge_constant_current():
    df = pd.DataFrame({"t_s": np.arange(0, 601, 1.0), "I_A": 1.0})
    assert charge_from_df(df) == pytest.approx(600.0)
    assert charge_at(df, 150) == pytest.approx(150.0)


def test_charge_rejects_bad_time():
    with pytest.raises(ValueError):
        charge_from_df(pd.DataFrame({"t_s": [0, 1, 1], "I_A": [1, 1, 1]}))
    with pytest.raises(ValueError):
        charge_from_df(pd.DataFrame({"t_s": [0, 1], "I_A": [1, np.nan]}))
    with pytest.raises(ValueError):
        charge_from_df(pd.DataFrame({"t_s": [0], "I_A": [1]}))


def test_dilution():
    assert undiluted_concentration(3.0, 1, 50) == pytest.approx(150.0)
    with pytest.raises(ValueError):
        undiluted_concentration(3.0, 10, 5)


def test_wide_x1_grid_recovers_high_efficiency():
    """Synthetic: x1 up to 1 with a realistic sigma (diluted DPD, ~2.5 mg/L undiluted)."""
    from chlorine import calculate_expected_chlorine
    from inference import run_inference
    F, M, V, Q, sigma = 96485.33212, 70.906, 0.5, 600.0, 2.5
    C = calculate_expected_chlorine(0.7, Q, F, 0.1, M, V)
    x = np.linspace(1e-3, 1.0, 1500)
    e = np.linspace(0.001, 0.6, 1500)
    _, med, lo, hi, _ = run_inference(C, V, F, M, Q, x, e, sigma=sigma)
    assert lo <= 0.7 <= hi
