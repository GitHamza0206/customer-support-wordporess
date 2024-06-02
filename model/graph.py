from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from IPython.display import Image, display

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


class Chatbot:
    def __init__(self):
        self.graph_builder = StateGraph(State)
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.graph_builder.add_node("chatbot", self.chatbot)
        self.graph_builder.set_entry_point("chatbot")
        self.graph_builder.set_finish_point("chatbot")
        self.graph = self.graph_builder.compile()


    def chatbot(self, state: State):
        return {"messages": [self.llm.invoke(state["messages"])]}

    def display_graph(self):

        try:
            display(Image(self.graph.get_graph().draw_mermaid_png()))
        except:
            # This requires some extra dependencies and is optional
            pass

    