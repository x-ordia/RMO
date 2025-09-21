from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel
from typing import List

def create_router(llm: BaseLanguageModel, topics: List[str], default_topic: str):
    """
    Creates a router that directs the conversation to the correct agent.

    Args:
        llm: The language model to use.
        topics: A list of topics that the agents can handle.
        default_topic: The default topic to use if the router cannot determine the topic.

    Returns:
        A function that takes the current state and returns the next node in the graph.
    """
    router_prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are an expert at routing a user question to a specialist. Your job is to route the user to the correct agent based on the user's question. The available agents are: {topics}. If the user's question is not related to any of these topics, you can route them to the '{default_topic}' agent."),
        ("human", "{question}"),
    ])
    router_chain = router_prompt | llm.bind(functions=[{
        "name": "route",
        "description": "Select the next agent to route to.",
        "parameters": {
            "type": "object",
            "properties": {
                "next": {
                    "type": "string",
                    "enum": topics + [default_topic],
                }
            },
            "required": ["next"],
        }
    }], function_call={"name": "route"})

    def router_function(state):
        return router_chain.invoke(state["messages"][-1].content).additional_kwargs["function_call"]["arguments"]["next"]
    
    return router_function