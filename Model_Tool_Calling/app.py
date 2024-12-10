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
    

@tool
def delete_database(name: str="database.db") -> str:
    """Deletes a database"""
    try:
        # Ensure the database file name ends with .db
        if not name.endswith(".db"):
            name += ".db"
        if os.path.exists(name):
            # Delete the database file
            os.remove(name)
            return f"Database '{name}' has been successfully deleted."
        else:
            return f"Database '{name}' does not exist in the current directory."

    except Exception as e:
        # Return error message in case of failure
        return f"An error occurred while deleting the database: {str(e)}"

@tool
def list_databases() -> str:
    """Lists all database files in the current directory."""
    try:
        # Get all files in the current directory
        files = os.listdir()
        # Filter files ending with .db
        db_files = [file for file in files if file.endswith(".db")]

        if db_files:
            return f"The current directory contains the following databases: \n {', '.join(db_files)}"
        else:
            return "No database files (.db) were found in the current directory."
    except Exception as e:
        return f"An error occurred while listing databases: {str(e)}"

@tool
def create_table(database_name: str, table_name: str, **columns: dict) -> str:
    """Creates a new table in the specified database."""
    try:
        
        files = os.listdir()
        # Filter files ending with .db
        db_files = [file for file in files if file.endswith(".db")]
        print(db_files)
        database_name = database_name.lower() + ".db"
        if database_name in db_files:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            print(columns)
            col = []
            for column_name, column_type in columns['columns'].items():
                print(f"Column Name: {column_name}, Column Type: {column_type['type']}")
                col.append(f"{column_name} {column_type['type'].upper()}")
            col = ", ".join(col)
            print(col)
            print("-------------------")
            cursor.execute(f"""
                           CREATE TABLE {table_name} (
                            id INTEGER PRIMARY KEY,
                            {col},
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """)
            conn.commit()
            conn.close()
            return f"Table '{table_name}' has been successfully created in the database '{database_name}'."
        else:
            return f"Database '{database_name}' does not exist in the current directory."
    except Exception as e:
        return f"An error occurred while creating the table: {str(e)}"





tools = [add, multiply, subtract, add_new_user, create_database, delete_database, list_databases, create_table]


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
            "create_database": create_database,
            "delete_database": delete_database,
            "list_databases": list_databases,
            "create_table": create_table
            }
        print("Bot: \n")
        selected_tool = tools_dict[tool_call["name"].lower()]
        tool_response = selected_tool.invoke(tool_call)
        print(f"tool response : \n{tool_response.content} ")
        message.append(tool_response)
        
    print(llm_with_tools.invoke(message).content)