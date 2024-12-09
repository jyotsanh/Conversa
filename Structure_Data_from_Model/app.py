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


from typing import Optional
from typing_extensions import Annotated, TypedDict
from pydantic import BaseModel, Field


# Pydantic

# TypedDict
class Joke(TypedDict):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]

    # Alternatively, we could have specified setup as:

    # setup: str                    # no default, no description
    # setup: Annotated[str, ...]    # no default, no description
    # setup: Annotated[str, "foo"]  # default, no description

    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]
    


structured_llm = model.with_structured_output(Joke)

print(structured_llm.invoke("Tell me a dad joke "))