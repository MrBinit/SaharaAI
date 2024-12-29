from langchain_ollama import ChatOllama
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_core.tools import Tool
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_experimental.graph_transformers import LLMGraphTransformer
from retrievers.hybrid_search import retrieve_documents_from_qdrant
from dotenv import load_dotenv
import os
from prompt_templates.prompt import CUSTOM_PROMPT
from retrievers.neo4j_graph import query_similarity_search

load_dotenv()

google_api_key = os.getenv("Google_API_key")
google_cse_id = os.getenv("GOOGLE_CSE_ID")

def graph_transformer_tool(text):
    graph_transformer = LLMGraphTransformer()
    graph = graph_transformer.transforme(text)
    return graph
def qdrant_retriever(query:str):
    docs_with_score = retrieve_documents_from_qdrant(query)
    return docs_with_score
def knowledge_graph(query:str):
    result = query_similarity_search(query)
    return result

# google wrapper
search = GoogleSearchAPIWrapper(google_api_key=google_api_key, google_cse_id = google_cse_id, k = 10)
tools = [
    # Tool(
    #     name = "google_search",
    #     description= "Search about Nepal's History. If the query is non-Historical tell I don't know and don't search in the Internet",
    #     func = search.run,
    #     ),
    Tool(
        name = "qdrant_retriever",
        description= "Retrieves relevant historical documents from Qdrant vector store for a given query.",
        func=qdrant_retriever,
    ),
    # Tool(
    #     name = "graph transformer",
    #     description = "Transforms input text into a graph representiation using LLMGraphTransformer",
    #     func = graph_transformer_tool,
    # ),
    # Tool(
    #     name = "knowledge_graph",
    #     description = "Retrieves relevent relationship among entities from the historical document from knowledge graph for a given query",
    #     func= knowledge_graph,
    # )

]

llm = ChatOllama(
    model = "llama3.2:3b",
    temperature = 0, 
    verbose= False, 
    base_url="http://ollama:11434"
)

memory = ChatMessageHistory(session_id = "test-session")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CUSTOM_PROMPT),
        ("human", "{input}"),
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

# memory in agent
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_message_key = "input",
    history_messages_key = "chat_history"

)
result = agent_with_chat_history.invoke({"input" : "Tell me about sugauli treaty"},
                                        config={"configurable": {"session_id": "test-session"}},

                                        )

if result:
    print(f"[Output] --> {result['output']}")
else:
    print('There is no result.')