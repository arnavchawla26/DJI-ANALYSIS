import numpy as np
import pandas as pd
import pytest

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backtester.backtest import run_backtest
from backtester.data import generate_synthetic_series
from backtester.grid_search import best_by_sharpe, grid_search
from backtester.strategy import sma_crossover_signal


def make_trending_prices(n=100, start=100.0, daily_return=0.01):
    dates = pd.bdate_range("2024-01-01", periods=n)
    prices = start * (1 + daily_return) ** np.arange(n)
    return pd.Series(prices, index=dates, name="Close")


def test_sma_crossover_rejects_bad_windows():
    prices = make_trending_prices(50)
    with pytest.raises(ValueError):
        sma_crossover_signal(prices, fast=20, slow=10)


def test_sma_crossover_rejects_insufficient_data():
    prices = make_trending_prices(10)
    with pytest.raises(ValueError):
        sma_crossover_signal(prices, fast=5, slow=20)


def test_sma_crossover_no_lookahead():
    prices = make_trending_prices(60)
    position = sma_crossover_signal(prices, fast=5, slow=20)
    assert position.iloc[:20].sum() == 0
    assert set(position.unique()).issubset({0, 1})


def test_uptrend_produces_positive_return_when_long():
    prices = make_trending_prices(120, daily_return=0.01)
    position = sma_crossover_signal(prices, fast=5, slow=20)
    result = run_backtest(prices, position, fast=5, slow=20)
    assert result.total_return_pct > 0
    assert result.num_trades >= 1


def test_flat_prices_produce_zero_return():
    dates = pd.bdate_range("2024-01-01", periods=60)
    prices = pd.Series([100.0] * 60, index=dates, name="Close")
    position = sma_crossover_signal(prices, fast=5, slow=20)
    result = run_backtest(prices, position, fast=5, slow=20)
    assert result.total_return_pct == pytest.approx(0.0, abs=1e-9)
    assert result.num_trades == 0


def test_max_drawdown_is_nonpositive():
    prices = generate_synthetic_series(n_days=500, seed=1)
    position = sma_crossover_signal(prices, fast=10, slow=50)
    result = run_backtest(prices, position, fast=10, slow=50)
    assert result.max_drawdown_pct <= 0


def test_grid_search_runs_and_ranks():
    prices = generate_synthetic_series(n_days=400, seed=7)
    results = grid_search(prices, fast_range=range(5, 15, 5), slow_range=range(20, 40, 10))
    assert len(results) > 0
    top = best_by_sharpe(results, top_n=3)
    assert len(top) <= 3
    sharpes = [r.sharpe for r in top]
    assert sharpes == sorted(sharpes, reverse=True)


def test_synthetic_series_is_reproducible():
    a = generate_synthetic_series(n_days=100, seed=99)
    b = generate_synthetic_series(n_days=100, seed=99)
    pd.testing.assert_series_equal(a, b)
