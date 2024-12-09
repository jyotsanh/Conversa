from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from langchain_core.tools import tool
import os
import sqlite3

# Load environment variables
load_dotenv()


model = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY"),
    )


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return f"{a} + {b} = {a + b}"


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return f"{a} * {b} = {a * b}"

@tool
def subtract(a: int, b: int) -> int:
    """Subtracts b from a."""
    return f"{a} - {b} = {a - b}"

@tool
def add_new_user(name: str, age: str="0") -> str:
    """Adds a New User into the Database"""
    return f"{name} user with age {age} has been added"

@tool
def create_database(name: str="database.db") -> str:
    """Creates a new database"""
    try:
        # Ensure the database file name ends with .db
        if not name.endswith(".db"):
            name += ".db"

        # Create the database
        conn = sqlite3.connect(name)
        conn.close()
         # Return success message
        return f"Database '{name}' has been successfully created at {os.path.abspath(name)}."
    except Exception as e:
        # Return error message in case of failure
        return f"An error occurred while creating the database: {str(e)}"
    return f"Database '{name}' has been successfully created at {os.path.abspath(name)}."
    



tools = [add, multiply, subtract, add_new_user,create_database]


llm_with_tools = model.bind_tools(tools)


while True:
    
    query = input("User: \n")
    if query == "q" or query == "Q":
        break
    message = [
        HumanMessage(query)
    ]
    ai_msg = llm_with_tools.invoke(message)
    message.append(ai_msg)


    for tool_call in ai_msg.tool_calls:
        # selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
        # tool_msg = selected_tool.invoke(tool_call)
        print(tool_call)
        # message.append(tool_msg)
        tools_dict = {
            "add": add, 
            "multiply": multiply,
            "subtract": subtract,
            "add_new_user": add_new_user,
            "create_database": create_database
            }
        selected_tool = tools_dict[tool_call["name"].lower()]
        tool_response = selected_tool.invoke(tool_call)
        print(tool_response.content)
        message.append(tool_response)
        
    print(llm_with_tools.invoke(message).content)