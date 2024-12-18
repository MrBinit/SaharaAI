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
                    docs.append(Document(page_content=content, metadata={"filename": filename}))
            else:
                print(f"Skipped non-txt file: {filename}")
    except Exception as e:
        print(f"Error reading documents from folder: {e}")
    return docs


def retrieval_from_graph(documents):
    if not documents:
        print("No documents were loaded. Exiting the process")
        return  None

    try:
        embedding_model = OllamaEmbeddings(model="mxbai-embed-large")
        print("Embedding model initialized successfully.")
    except Exception as e:
        print(f"Error initializing the embedding model: {e}")
        return  None

    try:
        vectorstore = Neo4jVector.from_documents(
            embedding=embedding_model,
            documents=documents,
            url=url,
            username=username,
            password=password
            ,
        )
        print("Documents successfully embedded and stored in Neo4j.")
        return vectorstore
    except Exception as e:
        print(f"Error storing documents in Neo4j: {e}")
        return  None 

def similarity_search(vectorstore, query):
    try:
        docs_with_score = vectorstore.similarity_search_with_score(query, k=2)
        for doc, score in docs_with_score:
            print(f"Document: {doc.page_content}\nScore: {score}")
    except Exception as e:
        print(f"Error during similarity search: {e}")

def query_similarity_search(query ):
    documents = read_documents(chunked_folder_path)
    if not documents:
        print("No document found in the folder")
        return
    vectorstore = retrieval_from_graph(documents)

    if not vectorstore:
        print("Failed to create vector store")
        return 
    result =similarity_search(vectorstore, query)
    return result
if __name__ == "__main__":
    query = "Who is King Birendra"
    query_similarity_search(query)

# store = Neo4jVector.from_existing_index()
# hybrid_db = Neo4jVector.from_documents()