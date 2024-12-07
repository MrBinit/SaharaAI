from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
import os
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import FastEmbedSparse, RetrievalMode
load_dotenv()

chunked_folder_path = os.getenv("CHUNK_FOLDER_PATH")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")

try:
    sparse_embedding = FastEmbedSparse(model_name = "Qdrant/bm25")
    print("Loaded sparse embedding successfully")
except Exception as e:
    print(f"Error while loading sparse embeddings: {e}")

try:
    embedding_model = OllamaEmbeddings(model = "mxbai-embed-large")
    print("Embedding model initialized successfully.")
except Exception as e:
    print(f"Error initializing the embedding model: {e}")
    exit(1)

client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

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

def add_document_to_qdrant(docs, collection_name = "History_Nepal"):
    try:
        client.delete_collection(collection_name=collection_name)
        print("Deleted existing Qdrant collection: History_Nepal")
        client.create_collection(
            collection_name= "History_Nepal",
            vectors_config=VectorParams(size = 1024, distance = Distance.COSINE)
        )
        print("Qdrant collection recreated successfully with 1024 dimensions.")

        qdrant = QdrantVectorStore.from_documents(
            documents= docs,
            embedding=embedding_model,
            sparse_embedding=sparse_embedding,  
            sparse_vector_name = "sparse-vector",
            url=qdrant_url,  
            prefer_grpc=True,
            api_key=qdrant_api_key,
            force_recreate= True,
            collection_name="History_Nepal",
            retrieval_mode=RetrievalMode.HYBRID,
        )
        print("Added documents to Qdrant")
    except Exception as e:
        print(f"Error while populating data into Qdrant: {e}")

def retrieve_documents_from_qdrant(query, k=2, collection_name="History_Nepal"):
    vector_store = QdrantVectorStore(
    client = client,
    collection_name=collection_name,
    embedding= embedding_model
    )
    docs_with_score = vector_store.similarity_search(query, k=2)
    results = []
    for doc in docs_with_score:
        result = {
            "content": doc.page_content,
            "score": doc.metadata.get("score", "No score available")
        }
        results.append(result)
    return results

docs = read_documents(chunked_folder_path)

if not docs:
    print("No documents were loaded. Exiting the process.")
    exit(1)

add_document_to_qdrant(docs)
