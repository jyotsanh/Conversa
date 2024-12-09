"""
Langchain code
"""
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os


load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")


model = ChatGroq(
    model="llama3-8b-8192",
    api_key=groq_api_key
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        # Our application now has two parameters-- the input 'messages' and 'language'
        MessagesPlaceholder(variable_name="messages"),
    ]
)

"""
langgraph code
"""
from typing import Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from typing_extensions import Annotated, TypedDict

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str
    
    
# Define a new graph
workflow = StateGraph(state_schema=State)
# workflow = StateGraph(state_schema=MessagesState) -> old workflow 




# Define the function that calls the model
def call_model(state: State):
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node(
            "model", 
            call_model
            )

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)



"""
input_messages = [
    HumanMessage("Hi my name is Bob!")
]



app.invoke({"messages":input_messages},config)

input_messages_2 = [
    HumanMessage("What's my name ?")
]
response = app.invoke({"messages":input_messages_2},config)


print(response['messages'][-1].pretty_print())
"""

print("press 'q' to exit")
config = {"configurable": {"thread_id": "abc123"}}
language = "Nepali"
while True:
    user_query = input("User: \n")
    if user_query=='q' or user_query=='Q':
        break
    
    input_messages = [
        HumanMessage(user_query)
    ]
    print("Bot: ")
    response = app.invoke(
            {
                "messages":input_messages,
                "language":language,
            },
            config,
        )
    print(response['messages'][-1].content)