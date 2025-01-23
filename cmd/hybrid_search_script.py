# this  code will execute hybrid script and create qdrant database
from dotenv import load_dotenv
import os
from retrievers.hybrid_search import read_documents, add_document_to_qdrant

load_dotenv()

chunked_folder_path = os.getenv("CHUNK_FOLDER_PATH")

if __name__ == "__main__":
    docs = read_documents(chunked_folder_path)
    
    if not docs:
        print("No documents were loaded. Exiting the process.")
        exit(1)
    
    add_document_to_qdrant(docs)