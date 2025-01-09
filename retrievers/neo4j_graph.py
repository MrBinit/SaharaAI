from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
import os
from dotenv import load_dotenv
from langchain.schema import Document

load_dotenv()

URI = os.getenv("NEO4J_URL")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
chunked_folder_path = os.getenv("CHUNK_FOLDER_PATH")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
index = "vector"
keyword_index_name = "keyword"

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
    try:
        embedding_model = OllamaEmbeddings(model="mxbai-embed-large", base_url=ollama_base_url)
        print("Embedding model initialized successfully.")
    except Exception as e:
        print(f"Error initializing the embedding model: {e}")
        return  None
    
    try:
        vectorstore = Neo4jVector.from_existing_index(
            embedding=embedding_model,
            url=URI,
            username=username,
            password=password,
            search_type="hybrid",
            index_name = index,
            keyword_index_name=keyword_index_name,
            node_label=["Events", "Person", "Place", "Dynasty", "Artifact", "Concept", "Era", "Organization"],
            embedding_node_property="embedding",
        )
        print("Successfully connected to the existing Neo4j vector index.")
        return vectorstore
    except Exception as e:
        print(f"Existing index not found, Creating a new one ......: {e}")

    documents = read_documents(chunked_folder_path)
    if not documents:
        print("No documents were loaded. Cannot create index")
        return  None
    try:
        vectorstore = Neo4jVector.from_documents(
            embedding=embedding_model,
            documents=documents,
            url=URI,
            username=username,
            password=password,
            search_type="hybrid",
            index_name = index,
            keyword_index_name=keyword_index_name,
            node_label = ["Events", "Person", "Place", "Dynasty", "Artifact", "Concept", "Era", "Organization"],
            embedding_node_property="embedding",
        )
        print("New vector index created successfully")
        return vectorstore
    except Exception as creation_error:
        print(f"Error creating vector index: {creation_error}")



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



