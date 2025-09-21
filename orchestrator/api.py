import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from orchestrator.main import create_graph

# Load environment variables from .env file
load_dotenv()

# Create the FastAPI app
app = FastAPI()

# Pydantic model for the request body
class StreamRequest(BaseModel):
    message: str

# Create and compile the graph once when the app starts
graph = create_graph()

# Async generator to stream the graph'''s output
async def stream_generator(input_message: str):
    """
    Streams the output from the LangGraph orchestrator.
    """
    # The input to the graph is a dictionary with a list of messages
    inputs = {"messages": [HumanMessage(content=input_message)]}

    # Use astream_events to get a stream of events from the graph
    # We can filter these events to get the output we want
    async for event in graph.astream_events(inputs, version="v1"):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Yield the content of the stream
                yield content
        elif kind == "on_tool_end":
            # Yield the output of the tool
            yield f"\nTool output: {event['data']['output']}\n"


@app.post("/orchestrate")
async def orchestrate(request: StreamRequest):
    """
    Takes a message and streams the orchestrator'''s response.
    """
    return StreamingResponse(stream_generator(request.message), media_type="text/plain")
