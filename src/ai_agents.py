import os
import yfinance as yf
from agno.agent import Agent
from agno.models.google import Gemini


# Config
def set_api_key(api_key: str):
    """Set Google API key dynamically from Streamlit input"""
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key


# Data helpers
def compare_stocks(symbols):
    """
    Compare stock % performance over 6 months
    """
    data = {}

    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="6mo")

            if hist.empty:
                continue

            data[symbol] = hist["Close"].pct_change().sum()

        except Exception:
            continue

    return data


def get_company_info(symbol):
    stock = yf.Ticker(symbol)

    return {
        "name": stock.info.get("longName", "N/A"),
        "sector": stock.info.get("sector", "N/A"),
        "market_cap": stock.info.get("marketCap", "N/A"),
        "summary": stock.info.get("longBusinessSummary", "N/A"),
    }


def get_company_news(symbol):
    stock = yf.Ticker(symbol)
    return stock.news[:5] if stock.news else []



# Agents
def get_market_analyst():
    return Agent(
        model=Gemini(id="gemini-flash-latest"), 
        description="Analyzes and compares stock performance.",
        instructions=[
            "Compare stock performance data provided.",
            "Rank stocks based on returns.",
            "Highlight outperformers and underperformers."
        ],
        markdown=True
    )


def get_company_researcher():
    return Agent(
        model=Gemini(id="gemini-flash-latest"),
        description="Analyzes company fundamentals and news.",
        instructions=[
            "Summarize company profile clearly.",
            "Highlight key business areas and risks.",
            "Summarize recent news and investor relevance."
        ],
        markdown=True
    )


def get_stock_strategist():
    return Agent(
        model=Gemini(id="gemini-flash-latest"),
        description="Provides investment recommendations.",
        instructions=[
            "Analyze market trends and company fundamentals.",
            "Evaluate risk vs return.",
            "Recommend best stocks with justification."
        ],
        markdown=True
    )


def get_team_lead():
    return Agent(
        model=Gemini(id="gemini-flash-latest"),
        description="Generates final investment report.",
        instructions=[
            "Combine all analyses into a structured report.",
            "Rank stocks clearly.",
            "Provide investor-friendly insights."
        ],
        markdown=True
    )


def get_quant_advisor():
    return Agent(
        model=Gemini(id="gemini-flash-latest"),
        description="Bridges quantitative finance with AI insights.",
        instructions=[
            "Analyze portfolio weights and diversification.",
            "Evaluate expected returns and volatility.",
            "Explain Sharpe ratio meaning.",
            "Identify risks and concentration issues.",
            "Suggest improvements."
        ],
        markdown=True
    )


# AI functions
def get_market_analysis(symbols):
    analyst = get_market_analyst()
    performance_data = compare_stocks(symbols)

    if not performance_data:
        return "No valid stock data found."

    response = analyst.run(
        f"Compare these stock performances: {performance_data}"
    )

    return response.content


def get_company_analysis(symbol):
    researcher = get_company_researcher()

    info = get_company_info(symbol)
    news = get_company_news(symbol)

    response = researcher.run(
        f"""
        Company: {info['name']}
        Sector: {info['sector']}
        Market Cap: {info['market_cap']}

        Summary:
        {info['summary']}

        Recent News:
        {news}

        Provide a clear investor-focused analysis.
        """
    )

    return response.content


def get_stock_recommendations(symbols):
    strategist = get_stock_strategist()

    market_analysis = get_market_analysis(symbols)

    company_data = {}
    for symbol in symbols: 
        company_data[symbol] = get_company_analysis(symbol)

    response = strategist.run(
        f"""
        Market Analysis:
        {market_analysis}

        Company Insights:
        {company_data}

        Which stocks would you recommend and why?
        """
    )

    return response.content


def get_final_investment_report(symbols):
    team_lead = get_team_lead()

    market_analysis = get_market_analysis(symbols)
    company_analyses = [get_company_analysis(s) for s in symbols]
    recommendations = get_stock_recommendations(symbols)

    response = team_lead.run(
        f"""
        Market Analysis:
        {market_analysis}

        Company Analyses:
        {company_analyses}

        Recommendations:
        {recommendations}

        Generate a structured investment report.
        Rank stocks from best to worst.
        """
    )

    return response.content


# Quant + AI fusion
def get_quant_ai_insight(weights, expected_returns, volatility, sharpe):
    advisor = get_quant_advisor()

    response = advisor.run(
        f"""
        Portfolio Weights:
        {weights}

        Expected Returns:
        {expected_returns.to_dict()}

        Volatility:
        {volatility}

        Sharpe Ratio:
        {sharpe}

        Analyze:
        - Diversification quality
        - Risk concentration
        - Return potential
        - Weaknesses
        - Suggested improvements
        """
    )

    return response.content


def validate_forecasts_with_ai(summary_df):
    advisor = get_quant_advisor()

    response = advisor.run(
        f"""
        These are predicted returns from a forecasting model:

        {summary_df.to_dict()}

        Are these realistic?
        Highlight any over-optimistic or risky assumptions.
        """
    )

    return response.content