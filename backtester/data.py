"""Data loading helpers for the backtester.

The backtester works on any daily OHLCV series with at least a Date and
Close column. Point it at a CSV you've downloaded yourself (Yahoo Finance,
FRED's DJIA series, your broker's export, etc.), or use the bundled
synthetic sample for a quick demo run.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def load_csv(path: str, date_col: str = "Date", close_col: str = "Close") -> pd.Series:
    """Load a Close-price series from a CSV file, indexed by date.

    Expects at minimum a date column and a close-price column. Extra
    columns are ignored.
    """
    df = pd.read_csv(path)
    if date_col not in df.columns or close_col not in df.columns:
        raise ValueError(
            f"CSV must contain '{date_col}' and '{close_col}' columns; "
            f"found: {list(df.columns)}"
        )
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).set_index(date_col)
    series = df[close_col].astype(float)
    series.name = "Close"
    return series


def generate_synthetic_series(
    n_days: int = 2500,
    start_price: float = 30000.0,
    annual_drift: float = 0.07,
    annual_vol: float = 0.16,
    seed: int = 42,
) -> pd.Series:
    """Generate a reproducible synthetic daily price series.

    This is NOT real market data — it's a seeded geometric Brownian motion
    walk, sized roughly like the Dow (starting ~30000, ~16% annualized
    vol), used only so the demo and test suite have something deterministic
    to run against without a network call.
    """
    rng = np.random.default_rng(seed)
    dt = 1 / 252
    daily_drift = annual_drift * dt
    daily_vol = annual_vol * np.sqrt(dt)

    shocks = rng.normal(loc=daily_drift, scale=daily_vol, size=n_days)
    log_returns = shocks - 0.5 * daily_vol**2
    prices = start_price * np.exp(np.cumsum(log_returns))

    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=n_days)
    series = pd.Series(prices, index=dates, name="Close")
    return series
