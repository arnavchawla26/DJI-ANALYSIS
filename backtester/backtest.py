"""Core backtest engine: turns a position series into performance metrics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


@dataclass
class BacktestResult:
    fast: int
    slow: int
    total_return_pct: float
    cagr_pct: float
    sharpe: float
    max_drawdown_pct: float
    num_trades: int
    win_rate_pct: float

    def as_dict(self) -> dict:
        return {
            "fast": self.fast,
            "slow": self.slow,
            "total_return_pct": round(self.total_return_pct, 2),
            "cagr_pct": round(self.cagr_pct, 2),
            "sharpe": round(self.sharpe, 3),
            "max_drawdown_pct": round(self.max_drawdown_pct, 2),
            "num_trades": self.num_trades,
            "win_rate_pct": round(self.win_rate_pct, 2),
        }


def run_backtest(
    prices: pd.Series,
    position: pd.Series,
    fast: int,
    slow: int,
    annual_risk_free_rate: float = 0.0,
) -> BacktestResult:
    """Compute performance metrics for holding `position` against `prices`.

    `position` is expected to be 0/1 (flat/long), already shifted to avoid
    look-ahead bias (see strategy.sma_crossover_signal).
    """
    daily_returns = prices.pct_change().fillna(0.0)
    strategy_returns = daily_returns * position

    equity_curve = (1 + strategy_returns).cumprod()
    total_return_pct = (equity_curve.iloc[-1] - 1) * 100

    n_years = len(prices) / TRADING_DAYS_PER_YEAR
    cagr = equity_curve.iloc[-1] ** (1 / n_years) - 1 if n_years > 0 else 0.0
    cagr_pct = cagr * 100

    daily_rf = annual_risk_free_rate / TRADING_DAYS_PER_YEAR
    excess_returns = strategy_returns - daily_rf
    std = excess_returns.std()
    sharpe = (
        (excess_returns.mean() / std) * np.sqrt(TRADING_DAYS_PER_YEAR)
        if std > 0
        else 0.0
    )

    running_max = equity_curve.cummax()
    drawdown = (equity_curve - running_max) / running_max
    max_drawdown_pct = drawdown.min() * 100

    trade_starts = (position.diff() == 1).sum()
    num_trades = int(trade_starts)

    trade_pnls = _per_trade_pnls(strategy_returns, position)
    win_rate_pct = (
        100 * sum(1 for p in trade_pnls if p > 0) / len(trade_pnls)
        if trade_pnls
        else 0.0
    )

    return BacktestResult(
        fast=fast,
        slow=slow,
        total_return_pct=total_return_pct,
        cagr_pct=cagr_pct,
        sharpe=sharpe,
        max_drawdown_pct=max_drawdown_pct,
        num_trades=num_trades,
        win_rate_pct=win_rate_pct,
    )


def _per_trade_pnls(strategy_returns: pd.Series, position: pd.Series) -> list[float]:
    """Compound strategy returns within each contiguous long segment."""
    pnls: list[float] = []
    in_trade = False
    trade_growth = 1.0

    for pos, ret in zip(position, strategy_returns):
        if pos == 1:
            if not in_trade:
                in_trade = True
                trade_growth = 1.0
            trade_growth *= 1 + ret
        else:
            if in_trade:
                pnls.append(trade_growth - 1.0)
                in_trade = False

    if in_trade:
        pnls.append(trade_growth - 1.0)

    return pnls
