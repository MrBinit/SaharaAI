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


client = QdrantClient(path="/home/binit/HistoryOfNepal/qdrant")
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
    client.delete_collection(collection_name="History_Nepal")
    print("Deleted existing Qdrant collection: History_Nepal")
except Exception as e:
    print(f"Error deleting existing Qdrant collection: {e}")

try:
    client.create_collection(
        collection_name= "History_Nepal",
        vectors_config=VectorParams(size = 1024, distance = Distance.COSINE)
    )
    print("Qdrant collection recreated successfully with 1024 dimensions.")
except Exception as e:
    print(f"Error creating Qdrant collection: {e}")
    exit(1)

vector_store = QdrantVectorStore(
    client = client,
    collection_name="History_Nepal",
    embedding= embedding_model,
)
print("Qdrant vector store initialized successfully.")

try:
    qdrant = QdrantVectorStore.from_texts(
        texts = docs,
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


query = "Where is Nepal? "
docs_with_score = vector_store.similarity_search(query, k=2)

for doc, score in docs_with_score:
    source = doc.metadata.get('score', 'No score available')
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)     


