"""Exhaustive grid search over moving-average window pairs."""

from __future__ import annotations

import pandas as pd

from .backtest import BacktestResult, run_backtest
from .strategy import sma_crossover_signal


def grid_search(
    prices: pd.Series,
    fast_range: range,
    slow_range: range,
    min_gap: int = 1,
) -> list[BacktestResult]:
    """Run the crossover backtest for every valid (fast, slow) pair.

    `min_gap` requires slow >= fast + min_gap, so the two windows are
    meaningfully different. Pairs where the price history is too short for
    the slow window are skipped.
    """
    results: list[BacktestResult] = []

    for fast in fast_range:
        for slow in slow_range:
            if slow < fast + min_gap:
                continue
            if len(prices) <= slow:
                continue
            position = sma_crossover_signal(prices, fast, slow)
            result = run_backtest(prices, position, fast, slow)
            results.append(result)

    return results


def best_by_sharpe(results: list[BacktestResult], top_n: int = 10) -> list[BacktestResult]:
    return sorted(results, key=lambda r: r.sharpe, reverse=True)[:top_n]


def results_to_dataframe(results: list[BacktestResult]) -> pd.DataFrame:
    return pd.DataFrame([r.as_dict() for r in results])
