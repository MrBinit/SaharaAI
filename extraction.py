from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import re

parsed_document = "/home/binit/HistoryOfNepal/parsed_books/parsed_documents.md"
output_folder = "/home/binit/HistoryOfNepal/parsed_chunked/"

def load_parsed_document(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def loading_chunking(content):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=500, length_function=len)
    splits = text_splitter.split_text(content)
    chunked_documents = text_splitter.create_documents(splits)

    def clean_text(text):
        text = re.sub(r"https?://[^\s]+(?:\.com|\.org|\.net|\.edu|[a-zA-Z]{2,})", "", text)
        text = re.sub(r"([^\n]*\b(www|downloaded from|download).*?[^\n]*)", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\n+", " ", text)
        text = re.sub(r"\bpp\. \d+(-\d+)?\b", "", text)   
        text = re.sub(r"\s*subject to the [^\n]+", "", text)  
        text = re.sub(r"document \d+", "", text) 
        text = re.sub(r"\bDocument \d+\b", "", text)
        text = re.sub(r"[^\w\s.,!?0-9/-]", "", text)
        text = re.sub(r"\d+\s*-\s*[A-Za-z\s]+(\.{2,})\s*\d*", "", text) 
        text = re.sub(r"\b(BC|AD|BS|c\.)\b", lambda m: m.group(0), text)

        return text


    for doc in chunked_documents:
        doc.page_content = clean_text(doc.page_content)

    return chunked_documents

def saved_chunked_documents(chunked_documents, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    for i, doc in enumerate(chunked_documents):
        file_name = f"chunk_text{i+1}.txt"
        file_path = os.path.join(output_folder, file_name)
        
        with open(file_path, "w") as f:
            f.write(doc.page_content) 
            print(f"Saved {file_name} to {file_path}")

if __name__ == "__main__":
    content = load_parsed_document(parsed_document)
    chunk_doc = loading_chunking(content)
    saved_chunked_documents(chunk_doc, output_folder)
    print(f"Number of chunks created: {len(chunk_doc)}")
    print(chunk_doc[0].page_content if chunk_doc else "No chunks created")
