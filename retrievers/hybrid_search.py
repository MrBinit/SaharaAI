#hybrid RAG with both sparse and dense
from langchain_ollama import OllamaEmbeddings
import os
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import FastEmbedSparse, RetrievalMode
from langchain_cohere import CohereRerank


load_dotenv()

chunked_folder_path = os.getenv("CHUNK_FOLDER_PATH")
qdrant_url = os.getenv("QDRANT_URL")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")

try:
    sparse_embedding = FastEmbedSparse(model_name="Qdrant/bm25")
    print("Loaded sparse embedding successfully")
except Exception as e:
    print(f"Error while loading sparse embeddings: {e}")

try:
    embedding_model = OllamaEmbeddings(model="mxbai-embed-large", base_url=ollama_base_url)
    print("Embedding model initialized successfully.")
except Exception as e:
    print(f"Error initializing the embedding model: {e}")
    exit(1)

try:
    client = QdrantClient(url=qdrant_url)
    print("Connected to Qdrant successfully.")
except Exception as e:
    print(f"Error connecting to Qdrant: {e}")
    exit(1)

def read_documents(chunked_folder_path):
    docs = []
    try:
        for filename in os.listdir(chunked_folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(chunked_folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    doc_id = os.path.splitext(filename)[0]
                    docs.append(Document(page_content=content, metadata={"id": doc_id}))
        print(f"Loaded {len(docs)} documents from '{chunked_folder_path}'.")
    except Exception as e:
        print(f"Error reading documents from folder: {e}")
    return docs

def add_document_to_qdrant(docs, collection_name="History_Nepal"):
    try:
        existing_collections = client.get_collections()
        existing_collection_names = [col.name for col in existing_collections.collections]
        
        if collection_name not in existing_collection_names:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
            )
            print(f"Qdrant collection '{collection_name}' created successfully.")
        else:
            print(f"Qdrant collection '{collection_name}' already exists.")
        
        qdrant = QdrantVectorStore.from_documents(
            documents=docs,
            embedding=embedding_model,
            sparse_embedding=sparse_embedding,  
            sparse_vector_name="sparse-vector",
            url=qdrant_url,  
            prefer_grpc=False,
            force_recreate=True,  
            collection_name=collection_name,
            retrieval_mode=RetrievalMode.HYBRID,
        )
        print("Added documents to Qdrant")
    except Exception as e:
        print(f"Error while populating data into Qdrant: {e}")

def retrieve_documents_from_qdrant(query, k=10, collection_name="History_Nepal"):
    try:
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embedding_model,
        )
        docs_with_score = vector_store.similarity_search(query, k=k)
        cohere_rerank = CohereRerank(model="rerank-english-v2.0")
        documents = [Document(page_content=doc.page_content, metadata=doc.metadata) for doc in docs_with_score]
        reranked_docs = cohere_rerank.rerank(query=query, documents=documents)

        results = []
        for doc, reranked_score in zip(reranked_docs, cohere_rerank.scores):
            result = {
                "content": doc.page_content,
                "original_score": doc.metadata.get("score", "No score available"),
                "rerank_score" : reranked_score
            }
            results.append(result)
        return results
    except Exception as e:
        print(f"Error retrieving documents from Qdrant: {e}")
        return []

if __name__ == "__main__":
    docs = read_documents(chunked_folder_path)
    
    if not docs:
        print("No documents were loaded. Exiting the process.")
        exit(1)
    
    add_document_to_qdrant(docs)