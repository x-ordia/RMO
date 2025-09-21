from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models import BaseLanguageModel
from langchain.agents import create_structured_chat_agent, AgentExecutor
from orchestrator.tools import create_sql_query, create_support_ticket, get_support_ticket_details

def create_agent(llm: BaseLanguageModel, tools: list, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_structured_chat_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

def create_sql_agent(llm: BaseLanguageModel):
    tools = [create_sql_query]
    system_prompt = "You are a SQL expert. You can create SQL queries to answer questions about data."
    return create_agent(llm, tools, system_prompt)

def create_support_agent(llm: BaseLanguageModel):
    tools = [create_support_ticket, get_support_ticket_details]
    system_prompt = "You are a support agent. You can create and manage support tickets."
    return create_agent(llm, tools, system_prompt)