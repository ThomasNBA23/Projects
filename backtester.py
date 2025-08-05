#Backtester 1 underlying

from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

# === CONFIGURATION ===
TICKERS = ["AAPL"]  
DATA_PATH = Path("data")  
STOCK_PATH = DATA_PATH / "stocks"
RESULTS_PATH = DATA_PATH / "results"
RESULTS_PATH.mkdir(exist_ok=True)

RISK_FREE_RATE = 0.01
DAYS_TO_EXPIRY = 30
OPTION_FREQ_DAYS = 5
ROLLING_VOL_DAYS = 30
POSITION_SIZE = 1



# === Black-Scholes-Merton functions (call option) ===
def bsm_call_price(S, K, T, r, sigma):
    if S <= 0 or K <= 0 or sigma <= 0 or T <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call



def bsm_greeks(S, K, T, r, sigma):
    if S <= 0 or K <= 0 or sigma <= 0 or T <= 0:
        return (0, 0, 0, 0, 0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 252
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    return delta, gamma, theta, vega, rho



#Backtester
def backtest_ticker(ticker, filepath):
    df = pd.read_csv(filepath, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    df["LogRet"] = np.log(df["Adj Close"] / df["Adj Close"].shift(1))
    df["Vol"] = df["LogRet"].rolling(ROLLING_VOL_DAYS).std() * np.sqrt(252)

    portfolio_value, daily_pnl, greeks_list = [], [], []
    open_positions = []
    last_trade_day = df["Date"].iloc[0] - pd.Timedelta(days=OPTION_FREQ_DAYS + 1)

    for i in range(len(df)):
        row = df.iloc[i]
        today, S, sigma = row["Date"], row["Adj Close"], row["Vol"]

        if np.isnan(sigma) or sigma == 0:
            portfolio_value.append(np.nan)
            daily_pnl.append(0)
            greeks_list.append((np.nan,) * 5)
            continue

        # Close expired options
        realized_pnl = 0
        still_open = []
        for pos in open_positions:
            pos["T"] -= 1 / 252
            if pos["T"] <= 0:
                final_value = max(S - pos["K"], 0)
                realized_pnl += (final_value - pos["premium"]) * POSITION_SIZE * 100
            else:
                still_open.append(pos)
        open_positions = still_open

        # New option if the previous expired
        if (today - last_trade_day).days >= OPTION_FREQ_DAYS:
            K = S
            T = DAYS_TO_EXPIRY / 252
            premium = bsm_call_price(S, K, T, RISK_FREE_RATE, sigma)
            delta, gamma, theta, vega, rho = bsm_greeks(S, K, T, RISK_FREE_RATE, sigma)
            open_positions.append({
                "K": K,
                "T": T,
                "premium": premium,
                "S_init": S
            })
            last_trade_day = today

        # Portfolio re-evaluation
        value = 0
        total_delta = total_gamma = total_theta = total_vega = total_rho = 0
        for pos in open_positions:
            price = bsm_call_price(S, pos["K"], pos["T"], RISK_FREE_RATE, sigma)
            delta, gamma, theta, vega, rho = bsm_greeks(S, pos["K"], pos["T"], RISK_FREE_RATE, sigma)
            value += price * POSITION_SIZE * 100
            total_delta += delta
            total_gamma += gamma
            total_theta += theta
            total_vega += vega
            total_rho += rho

        portfolio_value.append(value)
        daily_pnl.append(realized_pnl)
        greeks_list.append((total_delta, total_gamma, total_theta, total_vega, total_rho))

    # Save the results
    df["PortfolioValue"] = portfolio_value
    df["DailyPnL"] = daily_pnl
    df[["Delta", "Gamma", "Theta", "Vega", "Rho"]] = pd.DataFrame(greeks_list, index=df.index)
    df["CumulativePnL"] = df["DailyPnL"].cumsum()
    output_file = RESULTS_PATH / f"{ticker}_results.csv"
    df.to_csv(output_file, index=False)

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["CumulativePnL"], mode='lines', name='Cumulative PnL'))
    fig.update_layout(title=f"Backtest - {ticker} - Call ATM 30j",
                      xaxis_title="Date", yaxis_title="Profit (€)",
                      template="plotly_white")
    fig.show()



if __name__ == "__main__":
    for ticker in TICKERS:
        filepath = STOCK_PATH / f"{ticker}.csv"
        if filepath.exists():
            backtest_ticker(ticker, filepath)
        else:
            print(f"Fichier introuvable pour {ticker}: {filepath}")
