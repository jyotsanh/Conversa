from langchain_groq import ChatGroq

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

tools = [add, multiply]


agentic_model = model.bind_tools(tools)
print(agentic_model.invoke("What is 2 + 56 ? and what is 12 * 56 ?").tool_calls)