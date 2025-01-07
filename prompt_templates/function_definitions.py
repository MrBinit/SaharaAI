function_definitions = """[
    {
        "name": "knowledge_graph",
        "description": "Retrieve structured insights into relationships among historical entities, such as connections between people, events, or places in Nepalese history.",
        "parameters": {
            "type": "dict",
            "required": ["query"],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query describing the relationship or historical connection to explore."
                }
            }
        }
    },
    {
        "name": "qdrant_retriever",
        "description": "Retrieve detailed historical documents or narratives for a specific topic or event in Nepalese history. This function is ideal for obtaining in-depth descriptions or analyses.",
        "parameters": {
            "type": "dict",
            "required": ["query"],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query specifying the historical document or topic to retrieve."
                }
            }
        }
    },
    {
        "name": "google_search",
        "description": "Search the internet for supplementary information on Nepalese history, particularly for recent developments or additional details.",
        "parameters": {
            "type": "dict",
            "required": ["query"],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search term or phrase to find relevant information online."
                }
            }
        }
    }
]
"""
