from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from typing import Annotated
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class State(BaseModel):
    messages: Annotated[list, Field(default_factory=list), add_messages]
    user_query: str = Field(..., description="The user's support query")
    result: str = ""

def user_node(state):
    return {"messages": [HumanMessage(content=state.user_query)]}

def bot_node(state):
    return {
        "messages": [AIMessage(content="Hello, how can I help you?")],
        "result": "Support response generated."
    }

graph = StateGraph(State)
graph.add_node("user", user_node)
graph.add_node("bot", bot_node)
graph.add_edge("user", "bot")
graph.add_edge("bot", END)
graph.set_entry_point("user")

app = graph.compile()
final_state = app.invoke({"user_query": "I need help with my order."})
print(final_state["messages"])
print(final_state["result"])