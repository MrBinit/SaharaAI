---

## .env File

The `.env` file is used to store all sensitive configuration details and environment variables required for the project. These variables are used by the application to connect to external services, databases, and APIs.


Below is an example `.env` file configuration:

```env
# LLAMA Cloud API Keys
LLAMA_CLOUD_API_KEY=<YOUR_LLAMACLOUD_API_KEY>
LLAMA_CLOUD_API_KEY_2=<YOUR_LLAMACLOUD_API_KEY_2>

# Neo4j Database Configuration
NEO4J_URI=bolt://<YOUR_NEO4J_HOST>:<YOUR_NEO4J_PORT>
NEO4J_USERNAME=<YOUR_NEO4J_USERNAME>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>
AURA_INSTANCEID=<YOUR_AURA_INSTANCEID>
AURA_INSTANCENAME=<YOUR_AURA_INSTANCENAME>

# Folder Paths
CHUNK_FOLDER_PATH="/app/data/parsed_chunked"

# Google API Configuration
GOOGLE_API_KEY=<YOUR_GOOGLE_API_KEY>
GOOGLE_CSE_ID=<YOUR_GOOGLE_CSE_ID>

# Qdrant Configuration
QDRANT_API_KEY=<YOUR_QDRANT_API_KEY>
QDRANT_URL=<YOUR_QDRANT_URL>

# Ollama Base URL
OLLAMA_BASE_URL=<YOUR_OLLAMA_BASE_URL>

# Cohere API Key
COHERE_API_KEY=<YOUR_COHERE_API_KEY>

# Parsed Document Paths
parsed_document = "/app/data/parsed_books/parsed_documents.md"
output_folder = "/app/data/parsed_chunked"