import streamlit as st
import pandas as pd

from src.data_features import fetch_stock_data, prepare_for_prophet, compute_historical_returns, compute_expected_returns, build_forecast_summary
from src.prophet_model import forecast_stock
from src.portfolio import compute_covariance, optimize_portfolio

from src.ai_agents import set_api_key, get_final_investment_report, get_quant_ai_insight, validate_forecasts_with_ai

st.set_page_config(page_title="AI Portfolio Optimizer", layout="wide")

st.title("Stock Portfolio Optimizer")


# Sidebar
st.sidebar.header("Configuration")

tickers_input = st.sidebar.text_input("Enter stock tickers", value="AAPL,MSFT,GOOG")

tickers = [t.strip().upper() for t in tickers_input.split(",")]

forecast_days = st.sidebar.number_input("Forecast horizon (days)", min_value=1, max_value=90, value=30)

risk_free_rate = st.sidebar.number_input("Risk-free rate", min_value=0.0, max_value=0.2, value=0.0, step=0.001)

# AI API key
api_key = st.sidebar.text_input("Google API Key", type="password")
set_api_key(api_key)


# Session state
if "data_ready" not in st.session_state:
    st.session_state.data_ready = False


# Tabs
tab1, tab2, tab3 = st.tabs([
    "Portfolio Optimization",
    "AI Strategist",
    "AI + Quant Insights"
])


# Portfolio optimization tab
with tab1:
    st.header("Portfolio Optimization")

    if st.button("Run Optimization"):
        with st.spinner("Fetching data..."):
            data = fetch_stock_data(tickers)

        with st.spinner("Preparing data..."):
            prepared = {t: prepare_for_prophet(data[t]) for t in tickers}
            historical_returns = compute_historical_returns(data)

        with st.spinner("Forecasting..."):
            forecasts = {
                t: forecast_stock(prepared[t], periods=forecast_days)
                for t in tickers
            }
            mu = compute_expected_returns(forecasts)

        cov_matrix = compute_covariance(historical_returns)

        with st.spinner("Optimizing portfolio..."):
            optimal_portfolio = optimize_portfolio(
                mu,
                cov_matrix,
                risk_free_rate=risk_free_rate
            )

        # Saving to session state (Needed for AI tabs)
        st.session_state.data_ready = True
        st.session_state.optimal_portfolio = optimal_portfolio
        st.session_state.mu = mu
        st.session_state.summary_df = build_forecast_summary(
            data=data,
            forecasts=forecasts,
            forecast_days=forecast_days
        )

        # UI
        st.subheader("Optimized Portfolio Weights")

        weights_df = pd.DataFrame({
            "Ticker": tickers,
            "Weight": [optimal_portfolio["weights"][t] for t in tickers]
        })

        st.bar_chart(weights_df.set_index("Ticker"))

        st.write(f"Expected Return: {optimal_portfolio['expected_return']:.2%}")
        st.write(f"Volatility: {optimal_portfolio['volatility']:.2%}")
        st.write(f"Sharpe Ratio: {optimal_portfolio['sharpe_ratio']:.2f}")

        st.subheader("Forecast Summary per Ticker")
        st.dataframe(
            st.session_state.summary_df.style.format({
                "Last Price": "{:.2f}",
                "Expected Price": "{:.2f}",
                "Predicted Return (%)": "{:+.2f}%"
            }),
            use_container_width=True
        )

        with st.expander("Model Assumptions"):
            st.markdown("""
            - Expected returns from Prophet forecasts  
            - Risk from historical covariance  
            - Optimized for max Sharpe ratio  
            - No constraints or transaction costs  
            """)

# AI strategist tab
with tab2:
    st.header("AI Investment Strategist")

    if not api_key:
        st.warning("Please enter your API key in the sidebar.")
    else:
        if st.button("Generate AI Investment Report"):
            with st.spinner("AI analyzing market..."):
                report = get_final_investment_report(tickers)

            st.markdown(report)


# AI + quant insights
with tab3:
    st.header("AI + Quant Insights")

    if not st.session_state.data_ready:
        st.info("Run portfolio optimization first.")
    elif not api_key:
        st.warning("Please enter your API key.")
    else:
        col1, col2 = st.columns(2)

        
        # AI portfolio insight
        with col1:
            st.subheader("AI Portfolio Analysis")

            if st.button("Analyze Portfolio"):
                with st.spinner("AI analyzing portfolio..."):
                    insight = get_quant_ai_insight(
                        st.session_state.optimal_portfolio["weights"],
                        st.session_state.mu,
                        st.session_state.optimal_portfolio["volatility"],
                        st.session_state.optimal_portfolio["sharpe_ratio"]
                    )

                st.markdown(insight)

        # Forecast validation
        with col2:
            st.subheader("AI Forecast Validation")

            if st.button("Validate Forecasts"):
                with st.spinner("AI validating predictions..."):
                    validation = validate_forecasts_with_ai(
                        st.session_state.summary_df
                    )

                st.markdown(validation)
