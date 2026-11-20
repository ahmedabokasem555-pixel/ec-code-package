"""CSV helpers."""

import os

import numpy as np
import pandas as pd


def load_csv_data(file_path):
    """Read a CSV file into a DataFrame; raise FileNotFoundError if missing."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)


def validate_columns(df, required_columns):
    """Return True if all required columns exist, else raise ValueError listing the missing ones."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return True


def charge_from_df(df, t_col="t_s", i_col="I_A"):
    """Charge Q (coulombs) = trapezoidal integral of current (A) over time (s).

    Requires strictly increasing time, at least 2 rows, and no missing values. Use the measured
    current from the INA219 log, not the power-supply setting.
    """
    validate_columns(df, [t_col, i_col])
    t = df[t_col].to_numpy(dtype=float)
    i = df[i_col].to_numpy(dtype=float)
    if len(t) < 2:
        raise ValueError("Need at least 2 rows to integrate current")
    if not (np.isfinite(t).all() and np.isfinite(i).all()):
        raise ValueError("Time and current columns must not contain NaN/inf")
    if np.any(np.diff(t) <= 0):
        raise ValueError(f"{t_col} must be strictly increasing")
    return float(np.sum(0.5 * (i[1:] + i[:-1]) * np.diff(t)))


def charge_at(df, t_end, t_col="t_s", i_col="I_A"):
    """Charge accumulated up to time t_end (s), e.g. at the moment a DPD sample was taken."""
    sub = df[df[t_col] <= t_end]
    return charge_from_df(sub, t_col, i_col)


def undiluted_concentration(reading_mg_l, sample_ml, total_ml):
    """Concentration in the cell from a diluted DPD reading (sample_ml made up to total_ml)."""
    if reading_mg_l < 0 or sample_ml <= 0 or total_ml < sample_ml:
        raise ValueError("Need reading >= 0 and 0 < sample_ml <= total_ml")
    return reading_mg_l * total_ml / sample_ml
