from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from langchain_core.tools import tool
import os


# Load environment variables
load_dotenv()


model = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY"),
    )


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

@tool
def subtract(a: int, b: int) -> int:
    """Subtracts b from a."""
    return a - b


tools = [add, multiply, subtract]


llm_with_tools = model.bind_tools(tools)
query = "What is 3 * 12? Also, what is 11 + 49? and What is 11-8?"
message = [
    HumanMessage(query)
]
ai_msg = llm_with_tools.invoke(message)
message.append(ai_msg)


for tool_call in ai_msg.tool_calls:
    # selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    # tool_msg = selected_tool.invoke(tool_call)
    # print(tool_msg)
    # message.append(tool_msg)
    tools_dict = {
        "add": add, 
        "multiply": multiply,
        "subtract": subtract
        }
    selected_tool = tools_dict[tool_call["name"].lower()]
    tool_response = selected_tool.invoke(tool_call)
    message.append(tool_response)
    
print(llm_with_tools.invoke(message).content)