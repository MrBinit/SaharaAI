import pkg_resources

packages = [
    "langchain_ollama",
    "llama-index-core",
    "llama-parse",
    "llama-index-readers-file",
    "python-dotenv",
    "langchain-text-splitters",
    "langchain_google_community",
    "langchain-experimental",
    "langchain_qdrant",
    "cohere",
    "langchain_cohere",
    "uvicorn",
    "fastapi",
    "fastembed",
    "langchain",
    "neo4j",
    "psycopg2-binary",
    "sqlalchemy",
]

for package in packages:
    try:
        version = pkg_resources.get_distribution(package).version
        print(f"{package}: {version}")
    except pkg_resources.DistributionNotFound:
        print(f"{package}: Not installed")
