from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
import os
from dotenv import load_dotenv
from langchain.schema import Document

load_dotenv()

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
chunked_folder_path = os.getenv("chunk_folder_path")


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

docs = read_documents(chunked_folder_path)

if not docs:
    print("No documents were loaded. Exiting the process.")
    exit(1)

try:
    embedding_model = OllamaEmbeddings(model = "mxbai-embed-large")
    print("Embedding model initialized successfully.")
except Exception as e:
    print(f"Error initializing the embedding model: {e}")
    exit(1)

try:
    vectorstore = Neo4jVector.from_documents(
        embedding = embedding_model,
        documents = docs,
        url = url,
        username = username,
        password = password,
    )
    print("Documents successfully embedded and stored in Neo4j.")
except Exception as e:
    print(f"Error storing documents in Neo4j: {e}")
    exit(1)



query = "Where is Nepal? "
docs_with_score = vectorstore.similarity_search_with_score(query, k=2)

for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)     