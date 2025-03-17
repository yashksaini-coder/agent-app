import groq
import os
from dotenv import load_dotenv
load_dotenv()

# AI assistant imports
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.agent import Agent, RunResponse

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = groq.Client(api_key=GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError("Please provide a GROQ API key")


web_search_agent = Agent(
    name="web_agent",
    role="search the web for information based on the user given input",
    model=Groq(id="llama-3.1-8b-instant",api_key=GROQ_API_KEY),
    tools=[
        DuckDuckGoTools(search=True, news=True),

    ],
    instructions=[
        "Your job is to search and scrape the web for information based on the user queries",
        "your main objective is to provide exact information to the user available on the web",
    ]
)

financial_agent = Agent(
    name="financial_agent",
    role="get financial information",
    model=Groq(id="llama-3.1-8b-instant",api_key=GROQ_API_KEY),
    tools=[
        YFinanceTools(stock_price=True,
                    analyst_recommendations=True,
                    stock_fundamentals=True, 
                    company_info=True, 
                    technical_indicators=True, 
                    historical_prices=True,
                    key_financial_ratios = True,
                    income_statements = True,
                    ),
    ],
    instructions=[
        "You are a professional financial advisor AI agent",
        "your job is to provide financial information to users",
        "you can provide stock price, analyst recommendations, and stock fundamentals",
        "Provide information about companies, industries, and financial terms",
    ]
)

multi_ai = Agent(
    team=[web_search_agent, financial_agent],
    model=Groq(id="deepseek-r1-distill-llama-70b",api_key=GROQ_API_KEY),
    markdown=True,
)


multi_ai.print_response("Top news of 2024 till today with proper links to them ?",stream=True)
