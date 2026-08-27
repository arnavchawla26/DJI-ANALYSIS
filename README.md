# DJI Moving-Average Crossover Backtester

A real, working backtesting engine for simple moving-average crossover strategies, with an exhaustive grid search over fast/slow window pairs and standard performance metrics (total return, CAGR, Sharpe ratio, max drawdown, win rate).

This project previously shipped as just a README describing this idea with no implementation behind it. That's fixed now — the code below is real, tested, and runnable.

## What it does

1. Loads a daily Close-price series (from a CSV you provide, or a bundled synthetic series for demos).
2. For a range of fast/slow simple-moving-average window pairs, generates a long/flat position signal (long when the fast SMA is above the slow SMA), shifted by one day to avoid look-ahead bias.
3. Backtests each pair and reports total return, CAGR, Sharpe ratio, max drawdown, number of trades, and win rate.
4. Ranks all tested combinations by Sharpe ratio.

## Honesty note on data

This repo doesn't bundle real Dow Jones price history, and the sync/backtest tooling here has no network access to Yahoo Finance or similar providers. To backtest against the real Dow:

1. Download daily OHLC data yourself — e.g. Yahoo Finance's historical data export for `^DJI`, or FRED's `DJIA` series — as a CSV with at least `Date` and `Close` columns.
2. Point the CLI at it with `--csv path/to/file.csv`.

Without a CSV, `--sample` runs against a seeded synthetic price series (a random walk shaped roughly like the Dow) so you can see the engine work end-to-end without any external data. Results from `--sample` are **not** a claim about real market performance — they're there to prove the code runs and the tests pass.

## Getting Started

```sh
git clone https://github.com/arnavchawla26/DJI-ANALYSIS.git
cd DJI-ANALYSIS
pip install -r requirements.txt

# Quick demo, no external data needed:
python run_backtest.py --sample

# Real run against your own downloaded price history:
python run_backtest.py --csv data/dji_history.csv \
  --fast-min 5 --fast-max 60 --fast-step 5 \
  --slow-min 20 --slow-max 250 --slow-step 10 \
  --output results.csv
```

Widen the ranges (smaller steps, wider min/max) to scale up to a large exhaustive sweep — the engine itself has no hardcoded limit on how many combinations it evaluates, it's just a matter of runtime.

## Running the tests

```sh
python -m pytest tests/ -v
```

8 tests cover: signal validation (fast < slow, sufficient data), no-look-ahead-bias behavior, correct zero-return on flat prices, positive return on a synthetic uptrend, non-positive max drawdown, grid search ranking, and reproducibility of the synthetic data generator.

## Project Structure

```
backtester/
  data.py          # CSV loading + synthetic sample data generator
  strategy.py       # SMA crossover signal generation
  backtest.py        # performance metrics (return, CAGR, Sharpe, drawdown, win rate)
  grid_search.py      # exhaustive sweep over (fast, slow) pairs
run_backtest.py    # CLI entry point
tests/
  test_backtest.py  # pytest suite
```

## Limitations / Roadmap

- Long/flat only — no short positions, no position sizing, no transaction costs or slippage modeled yet.
- Grid search is currently over (fast, slow) window pairs only; adding stop-loss/take-profit or confirmation-day parameters would be a natural way to scale the sweep size further (the original idea behind this project referenced very large sweeps — that's straightforward to add as more grid dimensions in `grid_search.py`).
- No live/scheduled data pull — this is intentionally a batch analysis tool you point at a CSV.
