"""Layer 2: PERCEPTION. Read data and clean it. Bad text becomes NaN, not a crash."""
import time
import requests
import pandas as pd


def fetch(url, params=None, retries=3, timeout=30):
    """Get JSON from a web address. If it fails, wait 1s, 2s, 4s and try again."""
    for k in range(retries):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            time.sleep(2 ** k)
    raise RuntimeError(f"API unavailable after {retries} retries: {url}")


def clean(df, cols):
    """Turn the listed columns into numbers ('N/A' becomes NaN). Drop rows with no numbers."""
    df = df.copy()
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
    return df.dropna(subset=cols, how="all")


def load_csv(path, numeric):
    """Read a CSV file and clean the numeric columns."""
    return clean(pd.read_csv(path), numeric)
