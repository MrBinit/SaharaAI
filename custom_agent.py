from langchain_ollama import ChatOllama
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_google_community import GoogleSearchAPIWrapper

from dotenv import load_dotenv
import os

google_api_key = os.getenv("Google_API_key")

# google wrapper
search = GoogleSearchAPIWrapper(google_api_key= google_api_key)



# llm = ChatOllama(
#     model = "llama3.1",
#     temperature = 0, 
#     verbose= True
# )
# memory = ChatMessageHistory(session_id = "test-session")

# @tool
# def get_word_length(word: str) -> int:
#     """
#     This tool returns the length of a given word.
#     """
#     return len(word)

# tools = [get_word_length]

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are an Nepalese Historian who known detail history of Nepal.",
#         ),
#         ("user", "{input}"),
#         MessagesPlaceholder(variable_name = "agent_scratchpad"),

#     ]
# )

# llm_with_tools = llm.bind_tools(tools)

# agent = (
#     {
#         "input" : lambda x: x["input"],
#         "agent_scratchpad": lambda x: format_to_openai_tool_messages(
#             x["intermediate_steps"]
#        ),
#     }
#     | prompt
#     | llm_with_tools
#     | OpenAIToolsAgentOutputParser()
# )

# #Create an agent  executor by passing in the agent and tools
# agent_executor = AgentExecutor(agent = agent, tools = tools, verbose = True)

# # memory in agent
# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     lambda session_id: memory,
#     input_message_key = "input",
#     history_messages_key = "chat_history"

# )
# result = agent_with_chat_history.invoke({"input" :"Who is Prithvi Narayan Shah? "},
#                                         config={"configurable": {"session_id": "test-session"}},

#                                         )

# if result:
#     print(f"[Output] --> {result['output']}")
# else:
#     print('There is no result.')