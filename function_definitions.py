function_definitions = """[
    {{
        "name": "google_search",
        "description": "Search for information related to Nepalese History using Google Search. If the query is non-historical, this tool cannot be used.",
        "parameters": {{
            "type": "dict",
            "required": [
                "query"
            ],
            "properties": {{
                "query": {{
                    "type": "string",
                    "description": "The search query to retrieve information about Nepalese History."
                }}
            }}
        }}
    }},
    {{
        "name": "qdrant_retriever",
        "description": "Retrieve relevant historical documents from the Qdrant vector store for a given query.",
        "parameters": {{
            "type": "dict",
            "required": [
                "query"
            ],
            "properties": {{
                "query": {{
                    "type": "string",
                    "description": "The query to search for in the Qdrant vector store."
                }}
            }}
        }}
    }},
    {{
        "name": "graph_transformer",
        "description": "Transform input text into a graph representation using LLMGraphTransformer.",
        "parameters": {{
            "type": "dict",
            "required": [
                "text"
            ],
            "properties": {{
                "text": {{
                    "type": "string",
                    "description": "The input text to be transformed into a graph representation."
                }}
            }}
        }}
    }},
    {{
        "name": "knowledge_graph",
        "description": "Retrieve relationships among entities from historical documents using a knowledge graph.",
        "parameters": {{
            "type": "dict",
            "required": [
                "query"
            ],
            "properties": {{
                "query": {{
                    "type": "string",
                    "description": "The query to search for in the knowledge graph."
                }}
            }}
        }}
    }}
]
"""
