function_definitions = """[
    {
        "name": "knowledge_graph",
        "description": "Explore relationships among historical entities such as connections between people, events, or places. This function provides structured insights into these relationships.",
        "parameters": {
            "type": "dict",
            "required": [
                "query"
            ],
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
        "description": "Retrieve detailed historical documents or narratives for specific topics or events. It is useful for obtaining in-depth descriptions or analyses.",
        "parameters": {
            "type": "dict",
            "required": [
                "query"
            ],
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
        "description": "Search the internet for information on Nepalese History, particularly for recent developments or supplementary details.",
        "parameters": {
            "type": "dict",
            "required": [
                "query"
            ],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query term or phrase to search for relevant information."
                }
            }
        }
    }
]
"""
