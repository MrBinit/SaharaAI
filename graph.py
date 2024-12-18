from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
import os
from dotenv import load_dotenv
from langchain.schema import Document

load_dotenv()

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
chunked_folder_path = os.getenv("CHUNK_FOLDER_PATH")


def read_documents(chunked_folder_path):

    docs = []
    try:
        for filename in os.listdir(chunked_folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(chunked_folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    docs.append(Document(page_content=content, metadata={}))

    except Exception as e:
        print(f"Error reading documents from folder: {e}")
    return docs

def retrieval_from_graph(document):
    if not document:
        print("No document were loaded. Exiting the process")
    try:
        embedding_model = OllamaEmbeddings(model = "mxbai-embed-large")
        print("Embedding model initialized successfully.")
    except Exception as e:
        print(f"Error initializing the embedding model: {e}")
        exit(1)

    try:
        vectorstore = Neo4jVector.from_documents(
            embedding = embedding_model,
            documents = document,
            url = url,
            username = username,
            password = password,

        )
        print("Documents successfully embedded and stored in Neo4j.")
    except Exception as e:
        print(f"Error storing documents in Neo4j: {e}")
        exit(1)

if __name__ == "__main__":
    documents = read_documents(chunked_folder_path)
    retrieval_from_graph(documents)