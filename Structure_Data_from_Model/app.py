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



'''
A normal way to invoke the model


> messages = [
>    SystemMessage("Translate the following from English into Italian"),
>    HumanMessage("what is the meaning of life?"),
> ]

> print(model.invoke(messages).content)
''' 


'''
A invoke the model in streaming way


> messages = [
>    SystemMessage("Translate the following from English into Italian"),
>    HumanMessage("what is the meaning of life?"),
> ]

> for token in model.stream(messages):
>   print(token.content, end="|")
''' 
# 




"""
Prompt Templates

"""



### ChatPrompt Template doc:



"""
for dynamic creation of prompt , it creates a prompt like above mentioned
"""
from langchain_core.prompts import ChatPromptTemplate

system_template = "Translate the following from English into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template), 
        ("user", "{text}")
    ]
)

final_prompt = prompt_template.invoke({"language": "Italian", "text": "What is the capital of Nepal ?"})

print(f"prompt => \n {final_prompt}")

print(f"model response: \n {model.invoke(final_prompt).content}")
"""
@tool
def multiply(a: int, b: int) -> int:
    "Multiply a and b."
    return a * b

# Let's inspect some of the attributes associated with the tool.
print(multiply.name)
print(multiply.description)
print(multiply.args)

model.bind_tools(
    [
        
    ]
)

"""




