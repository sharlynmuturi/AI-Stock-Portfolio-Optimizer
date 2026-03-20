# AI Stock Portfolio Optimizer

A **quantitative portfolio optimization system** that combines **time-series forecasting** with **Modern Portfolio Theory (MPT)**, enhanced with **AI agents** to provide investment insights. The system is presented via a **Streamlit dashboard**.

It answers key investor questions:

1.  **Expected returns** per stock
    
2.  **Portfolio risk** based on historical covariance
    
3.  **Optimal capital allocation** balancing risk and return
    
4.  **AI-driven insights** on stocks and portfolio quality

## Disclaimer

This dashboard is for educational and informational purposes only. It does not constitute financial advice. Please verify results independently before making investment decisions.   

* * *

## Features

*   Forecasts **stock prices** using **Facebook Prophet**
    
*   Computes **expected returns** from forecasts
    
*   Estimates **risk** using historical volatility & covariance
    
*   Optimizes portfolio weights using **Sharpe ratio**
    
*   Provides **AI-driven market analysis, stock research, and portfolio advice**
    
*   Validates model forecasts with AI insights
    

* * *

## Project Structure

| File / Folder | Purpose |
| --- | --- |
| src/data_features.py | Functions for fetching historical stock data, computing returns, and preparing Prophet-ready data. |
| src/prophet_model.py | Prophet forecasting functions for future stock prices. |
| src/portfolio.py | Portfolio risk estimation (covariance) and Sharpe ratio-based optimization. |
| src/ai_agents.py | Defines AI agents for market analysis, company research, stock recommendations, portfolio analysis, and final report generation. Includes helper functions for Google API key handling and data preparation. |
| models.py | Lists and validates available Google Generative AI models for generateContent. Adjust models in ai_agents.py as necessary. |
| app.py | Main Streamlit dashboard. Runs portfolio optimization, AI strategist, and AI + Quant insights tabs. |

* * *

## Installation

1.  Clone the repo:
    
``` bash
git clone https://github.com/sharlynmuturi/AI-Stock-Portfolio-Optimizer.git  
cd AI-Stock-Portfolio-Optimizer
```
2.  Create a virtual environment:
    
``` bash
python -m venv venv  
venv\Scripts\activate # Windows
source venv/bin/activate # Linux/Mac  
```
3.  Install dependencies:
    
``` bash
pip install -r requirements.txt
```
4.  Create a `.env` file and add your **Google API key**:

Create an **API key** in the [Google Cloud Console](https://console.cloud.google.com/). Copy it into `.env` or input it in the Streamlit sidebar.
    
``` bash
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

* * *

## How It Works

### 1\. Portfolio Optimization

*   **Input**: Stock tickers, forecast horizon, risk-free rate
    
*   **Process**:
    
    *   Fetch historical data from Yahoo Finance
        
    *   Prepare data for Prophet
        
    *   Forecast future prices
        
    *   Compute expected returns
        
    *   Estimate risk via covariance matrix
        
    *   Optimize weights for maximum Sharpe ratio
        
*   **Output**: Portfolio weights, expected return, volatility, Sharpe ratio, forecast summary
    

### 2\. AI Investment Strategist

*   **Market Analysis**: Compares performance of multiple stocks
    
*   **Company Analysis**: Summarizes fundamentals and news
    
*   **Stock Recommendations**: Generates AI-backed stock picks
    
*   **Final Investment Report**: Combines analyses into structured, investor-friendly report
    

### 3\. AI + Quant Insights

*   **Portfolio Insights**: AI evaluates diversification, risk concentration, and expected returns
    
*   **Forecast Validation**: AI reviews Prophet predictions for realism and risk assessment
    

* * *

## Dashboard Layout

*   **Portfolio Optimization Tab**: Input tickers & parameters, see optimized weights and metrics
    
*   **AI Strategist Tab**: Generate AI investment report with market & company analysis
    
*   **AI + Quant Insights Tab**: Evaluate portfolio, validate forecasts and get AI suggestions
    

* * *

## Design Decisions

| Decision | Reason |
| --- | --- |
| Forecast prices, not returns | More stable for Prophet time-series modeling |
| Use forecast mean | Reduces noise in expected return estimation |
| Historical covariance | More robust than volatility forecasts |
| Optimize for Sharpe ratio | Industry standard for risk-adjusted return |
| No transaction costs | Simplicity and clarity |

* * *

## Limitations

### 1\. Data Limitations

*   **Yahoo Finance data** may have **missing days**, **dividends**, or **splits** that affect return calculations.
    
*   Historical data may contain **errors or noise**, which can influence risk estimation.
    
*   Limited to **daily price data**; intraday dynamics are not captured.
    

### 2\. Forecasting Limitations (Prophet)


*   Prophet assumes an **additive trend + seasonality structure**; sudden market shocks are not modeled.
    
*   Forecasts are **forward-looking expectations**, not guarantees; real returns may differ significantly.
    
*   Only **prices** are forecasted, **volatility/risk is not forecasted** — risk is derived from historical covariance.
    
*   Model does not account for **macro events, news sentiment, or geopolitical risks** unless AI agents are used separately.
    

### 3\. Portfolio Optimization Limitations


*   **No transaction costs** (commissions, slippage) are considered.
    
*   **No short-selling or leverage constraints**; portfolio weights are unconstrained beyond sum=1.
    
*   Risk is estimated from **historical covariance**, which may not reflect future correlations.
    
*   Optimized solely for **Sharpe ratio**, which may overemphasize return/risk and ignore other factors like liquidity or drawdowns.
    

### 4\. AI Integration Limitations


*   AI agents rely on **Google Generative AI models**, which may generate **approximate insights**.
    
*   Results are **only as good as the input data**; invalid tickers or missing info may lead to poor recommendations.
    
*   AI does not execute trades or validate strategies in real markets - purely **informational and analytical**.
    
*   Model outputs may include **over-optimistic or subjective language**, requiring user judgment.
    

### 5\. Computational and Practical Limitations


*   Prophet forecasts and AI queries can be **time-consuming for many tickers**.
    
*   Streamlit session state may **consume memory** if multiple runs are performed.
    
*   Real-time portfolio monitoring or dynamic rebalancing is **not implemented**.
    
* * *

## References

*   [Facebook Prophet Documentation](https://facebook.github.io/prophet/)
    
*   [Yahoo Finance API via yfinance](https://pypi.org/project/yfinance/)
    
*   [Google Generative AI](https://developers.generativeai.google/)
    
*   [Modern Portfolio Theory (Markowitz)](https://en.wikipedia.org/wiki/Modern_portfolio_theory)