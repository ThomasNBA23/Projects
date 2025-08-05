# 📈 Options Backtester – Black-Scholes Strategy

This project implements a Python-based **options backtester** using the **Black-Scholes-Merton (BSM)** model. It evaluates the performance of a systematic strategy that buys **at-the-money (ATM) European call options** with a 30-day maturity, rolling every few days.

---

## 🗃️ Data

The historical stock price data used in this project comes from a **Kaggle dataset**.  
Each CSV file contains daily adjusted closing prices (`Adj Close`) for a given ticker.

- Format: one CSV file per stock symbol (e.g., `AAPL.csv`)
- Required columns: at least `Date` and `Adj Close`

> 📁 Example file path: `data/stocks/AAPL.csv`

---

## ⚙️ Strategy Overview

- **Underlying**: Stock (e.g., AAPL)
- **Option type**: European Call (ATM)
- **Model**: Black-Scholes-Merton
- **Time to expiry**: 30 calendar days
- **Entry frequency**: Every 5 trading days
- **Volatility**: Rolling 30-day historical volatility (annualized)
- **Position size**: 1 options contract = 100 shares

---

## 📊 Outputs

For each ticker, the script generates:

- Daily portfolio value
- Daily realized PnL (from expired options)
- Greeks (Delta, Gamma, Theta, Vega, Rho)
- Cumulative PnL over time
- Interactive Plotly chart of the strategy performance
- Results saved as a CSV in: `data/results/{ticker}_results.csv`

---

## 🧠 Key Components

- `bsm_call_price()`: computes the theoretical price of a call option using the Black-Scholes model
- `bsm_greeks()`: calculates the option Greeks
- `backtest_ticker()`: main function that simulates the strategy for a given ticker

---

## ▶️ How to Run

1. Place your stock CSV files in `data/stocks/` (e.g., `AAPL.csv`)
2. Update the `TICKERS` list in the script to include your desired stocks
3. Run the script:

```bash
python backtester.py
