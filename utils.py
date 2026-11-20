"""CSV helpers."""

import os

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
