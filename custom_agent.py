from langchain_ollama import ChatOllama
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

llm = ChatOllama(
    model = "llama3.1",
    temperature = 0, 
    verbose= True
)

@tool
def get_word_length(word: str) -> int:
    """
    This tool returns the length of a given word.
    """
    return len(word)

tools = [get_word_length]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an Nepalese Historian who known detail history of Nepal.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name = "agent_scratchpad"),

    ]
)

llm_with_tools = llm.bind_tools(tools)

agent = (
    {
        "input" : lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
       ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

#Create an agent  executor by passing in the agent and tools
agent_executor = AgentExecutor(agent = agent, tools = tools, verbose = True)
result = agent_executor.invoke({"input" :"Who is Prithvi Narayan Shah? "})

if result:
    print(f"[Output] --> {result['output']}")
else:
    print('There is no result.')