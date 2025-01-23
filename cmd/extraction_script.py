# this will extract the parsed.md document and chunk them and store it into chunks. 
from preprocessing import load_parsed_document, loading_chunking, saved_chunked_documents
import os 
from dotenv import load_dotenv

load_dotenv()

parsed_document = os.getenv("parsed_document")
output_folder = os.getenv("output_folder")

if __name__ == "__main__":
    content = load_parsed_document(parsed_document)
    chunk_doc = loading_chunking(content)
    saved_chunked_documents(chunk_doc, output_folder)
    print(f"Number of chunks created: {len(chunk_doc)}")
    print(chunk_doc[0].page_content if chunk_doc else "No chunks created")
