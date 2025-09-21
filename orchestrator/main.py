import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from orchestrator.tools import yfinance_tool

def create_graph():
    # Replace ChatOpenAI with ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=os.getenv("GEMINI_API_KEY"))

    # Define the tools
    tools = [TavilySearch(max_results=3), DuckDuckGoSearchRun(), yfinance_tool]

    # Create the graph
    graph = create_react_agent(llm, tools)

    return graph