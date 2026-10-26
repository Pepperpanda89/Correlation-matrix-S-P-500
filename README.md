# S&P 500 Stock Correlation Visualizer

An interactive desktop app that shows **how closely S&P 500 stocks move together**, and what that means for diversifying a portfolio.

Tick the stocks you're interested in, choose how many years of history to use, and the app builds a correlation heatmap of their daily returns together with a plain-English diversification report.

## Features

- **~500 S&P 500 stocks** organised by sector, with live search by ticker, company or sector
- **Correlation heatmap** of daily returns for any selection of stocks
- **Portfolio analysis report**
  - most and least correlated pairs
  - top 5 lists and every negatively correlated pair
  - average correlation within each sector
  - an overall diversification assessment (high concentration risk / moderate / good)
- **Export**: save the heatmap (PNG), correlation matrix (CSV) and report (TXT)

## How it works

1. Downloads adjusted daily closing prices for the selected stocks
2. Converts prices to daily percentage returns
3. Computes the Pearson correlation between every pair of stocks

A correlation of **+1** means two stocks move in lockstep, **0** means no linear relationship and **−1** means they move in opposite directions. A portfolio of stocks with low correlation to each other is better diversified, so losses in one holding are less likely to coincide with losses in the others.

## Getting started

Requires Python 3.9+.

```bash
git clone https://github.com/Pepperpanda89/Correlation-matrix-S-P-500.git
cd Correlation-matrix-S-P-500
pip install -r requirements.txt
python stock_correlation.py
```

Price data is downloaded from Yahoo Finance via [`yfinance`](https://github.com/ranaroussi/yfinance), so an internet connection is needed.

## Built with

Python · tkinter · pandas · NumPy · matplotlib · seaborn · yfinance

## License

[MIT](LICENSE)
