"""Moving-average crossover signal generation."""

from __future__ import annotations

import pandas as pd


def sma_crossover_signal(prices: pd.Series, fast: int, slow: int) -> pd.Series:
    """Return a position series: 1 (long) when fast SMA > slow SMA, else 0.

    `fast` must be strictly less than `slow`. The signal is shifted forward
    one day so a crossover observed at the close of day T is only acted on
    starting day T+1 (no look-ahead bias).
    """
    if fast >= slow:
        raise ValueError(f"fast window ({fast}) must be < slow window ({slow})")
    if len(prices) <= slow:
        raise ValueError(
            f"need more than {slow} price points, got {len(prices)}"
        )

    fast_sma = prices.rolling(window=fast, min_periods=fast).mean()
    slow_sma = prices.rolling(window=slow, min_periods=slow).mean()

    raw_signal = (fast_sma > slow_sma).astype(int)
    position = raw_signal.shift(1).fillna(0).astype(int)
    position.name = f"position_{fast}_{slow}"
    return position
