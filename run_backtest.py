#!/usr/bin/env python3
"""CLI entry point for the moving-average crossover grid search.

Examples
--------
Quick demo run on synthetic sample data (no external data needed):

    python run_backtest.py --sample

Full run against your own downloaded price history:

    python run_backtest.py --csv data/dji_history.csv \\
        --fast-min 5 --fast-max 60 --fast-step 5 \\
        --slow-min 20 --slow-max 250 --slow-step 10

The default ranges below produce a modest grid for a fast demo; widen them
(e.g. --fast-step 1 --slow-step 1 over 5-100 / 20-260) to reproduce the kind
of large-scale sweep (tens of thousands of combinations) this project was
originally described as doing.
"""

from __future__ import annotations

import argparse
import sys

from backtester.data import generate_synthetic_series, load_csv
from backtester.grid_search import best_by_sharpe, grid_search, results_to_dataframe


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--csv", help="Path to a CSV with Date and Close columns")
    source.add_argument(
        "--sample",
        action="store_true",
        help="Use a bundled synthetic price series instead of real data (demo/testing only)",
    )

    parser.add_argument("--fast-min", type=int, default=5)
    parser.add_argument("--fast-max", type=int, default=30)
    parser.add_argument("--fast-step", type=int, default=5)
    parser.add_argument("--slow-min", type=int, default=20)
    parser.add_argument("--slow-max", type=int, default=100)
    parser.add_argument("--slow-step", type=int, default=10)
    parser.add_argument("--top", type=int, default=10, help="How many top results to print")
    parser.add_argument("--output", help="Optional path to write the full results grid as CSV")

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.sample:
        prices = generate_synthetic_series()
        print(
            "Using bundled SYNTHETIC sample data (not real market data) — "
            "pass --csv to run against real price history.\n"
        )
    else:
        prices = load_csv(args.csv)
        print(f"Loaded {len(prices)} price points from {args.csv}\n")

    fast_range = range(args.fast_min, args.fast_max + 1, args.fast_step)
    slow_range = range(args.slow_min, args.slow_max + 1, args.slow_step)

    results = grid_search(prices, fast_range, slow_range)
    if not results:
        print("No valid (fast, slow) pairs produced results — check your ranges and data length.")
        return 1

    print(f"Ran {len(results)} (fast, slow) combinations.\n")

    top = best_by_sharpe(results, top_n=args.top)
    df = results_to_dataframe(top)
    print(f"Top {len(top)} by Sharpe ratio:\n")
    print(df.to_string(index=False))

    if args.output:
        full_df = results_to_dataframe(results)
        full_df.to_csv(args.output, index=False)
        print(f"\nFull results ({len(full_df)} rows) written to {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
