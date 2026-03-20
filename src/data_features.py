import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Fetch historical stock data
def fetch_stock_data(tickers, years=3):
    end = datetime.today()
    start = end - timedelta(days=365 * years)
    data = {}
    invalid_tickers = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        try:
            df = stock.history(start=start, end=end, auto_adjust=True, actions=False)
            
            # Check for None or empty dataframe
            if df is None or df.empty:
                invalid_tickers.append(ticker)
                continue

            df.reset_index(inplace=True)
            data[ticker] = df

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            invalid_tickers.append(ticker)

    if invalid_tickers:
        print(f"Warning: No data for tickers: {', '.join(invalid_tickers)}")

    if not data:
        raise ValueError("No valid stock data fetched. Check your tickers or network.")

    return data


# Preparing Prophet input
def prepare_for_prophet(df):
    prophet_df = df[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
    
    # Removing timezone info if present
    prophet_df["ds"] = prophet_df["ds"].dt.tz_localize(None)
    
    return prophet_df


# Historical returns
def compute_historical_returns(data):
    return pd.DataFrame({
        ticker: df["Close"].pct_change().dropna()
        for ticker, df in data.items()
    })


# Expected returns from forecast
def compute_expected_returns(forecasts):
    return pd.Series({
        ticker: forecast["yhat"].pct_change().dropna().mean()
        for ticker, forecast in forecasts.items()
    })

def build_forecast_summary(data, forecasts, forecast_days):
    rows = []

    for ticker, df in data.items():
        last_price = df["Close"].iloc[-1]

        forecast = forecasts[ticker]
        expected_price = forecast["yhat"].iloc[-forecast_days:].mean()

        predicted_return = (expected_price - last_price) / last_price

        rows.append({
            "Ticker": ticker,
            "Last Price": round(last_price, 2),
            "Expected Price": round(expected_price, 2),
            "Predicted Return (%)": round(predicted_return * 100, 2)
        })

    return pd.DataFrame(rows)
