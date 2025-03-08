Financial Data Analysis of Dow Jones Industrial Average with Moving Averages

Overview

This project analyzes historical Dow Jones Industrial Average (DJIA) data using Python and financial analysis techniques. The goal is to evaluate the effectiveness of Moving Average Crossover strategies across multiple timeframes and identify optimal trading strategies for improved decision-making in financial markets.

Features

Data Extraction and Preprocessing: Pulls historical DJIA data from various sources, cleans, and prepares it for analysis.

Moving Average Crossover Strategy: Implements and tests different combinations of moving averages to identify the most effective strategy.

Multi-Timeframe Analysis: Examines 10 different timeframes (1min, 5min, 15min, 30min, 1hour, 1day, 1week, 1month, 3month, 1year) to compare strategy performance.

Backtesting: Tests over 1,000,000 strategy combinations using historical data to determine profitability.

Performance Metrics: Evaluates strategies based on key financial indicators, including return on investment (ROI), Sharpe ratio, maximum drawdown, and trade win rates.

Automated Reporting: Generates summary reports, charts, and graphs for visualization of strategy performance.

Installation

To set up and run the project on your local machine, follow these steps:

Prerequisites

Ensure you have the following installed:

Python (>=3.8)

pip (Python package manager)

Clone the Repository

git clone https://github.com/arnavchawla26/DJI-ANALYSIS.git
cd DJI-ANALYSIS

Install Required Dependencies

pip install -r requirements.txt

Usage

1. Fetch and Preprocess Data

python fetch_data.py

This script downloads and preprocesses historical DJIA data.

2. Run Moving Average Crossover Analysis

python moving_avg_crossover.py

This script applies moving average crossover strategies to test different configurations and outputs the best-performing strategies.

3. Run Backtesting

python backtest.py

Runs backtesting on historical data to evaluate the effectiveness of selected strategies.

4. Visualize Results

python visualize_results.py

Generates graphs and statistical reports for performance analysis.

Project Structure

DJI-ANALYSIS/
├── data/               # Raw and processed historical DJIA data
├── scripts/            # Python scripts for data processing, strategy testing, and visualization
├── results/            # Output reports, charts, and performance metrics
├── notebooks/          # Jupyter notebooks for exploratory analysis
├── requirements.txt    # List of dependencies
├── README.md           # Project documentation
├── .gitignore          # Ignore unnecessary files

Methodology

1. Data Collection

Historical DJIA data is collected from financial market APIs or CSV files.

Data is cleaned to remove inconsistencies and missing values.

2. Moving Average Strategies

Implements Simple Moving Averages (SMA) and Exponential Moving Averages (EMA).

Tests various combinations of short-term and long-term moving averages (e.g., 5-day vs. 20-day, 10-day vs. 50-day, etc.).

Determines buy and sell signals based on crossover points.

3. Backtesting and Performance Evaluation

Simulates past trades based on crossover signals.

Calculates performance metrics such as:

Return on Investment (ROI)

Sharpe Ratio

Maximum Drawdown

Win/Loss Ratio

Total Trades Executed

Outputs results in a structured format for analysis.

4. Multi-Timeframe Analysis

Runs tests across multiple timeframes to compare strategy effectiveness.

Identifies optimal strategies for different market conditions (short-term vs. long-term trading).

Results and Findings

The project tested over 1,000,000 strategy combinations across 10 different timeframes.

Optimal strategies were identified based on performance metrics.

Key Takeaways:

Short-term moving averages performed better in highly volatile conditions.

Long-term moving averages were more reliable for stable trends.

The best-performing strategy depended on the selected timeframe.

Future Improvements

Live Trading Integration: Implementing a feature to apply the best strategy in real-time using a trading API.

Machine Learning Enhancements: Using AI to optimize strategy selection based on market conditions.

Portfolio Diversification Analysis: Applying the method to multiple stock indices for broader insights.

Contributions

Contributions are welcome! Feel free to submit issues and pull requests.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Author

Arnav ChawlaGitHub: arnavchawla26

