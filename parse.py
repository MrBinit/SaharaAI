from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from pathlib import Path
import os 

load_dotenv()
api_key_1 = os.getenv("LLAMA_CLOUD_API_KEY")
api_key_2 = os.getenv("LLAMA_CLOUD_API_KEY_2")

parser = LlamaParse(
    result_type = "markdown",
    api_key= api_key_2
)
folder_path = "/home/binit/HistoryOfNepal/new_books"
file_extractor = {".pdf": parser}

pdf_files = [str(file) for file in Path(folder_path).rglob("*.pdf")]

documents = SimpleDirectoryReader(input_files = pdf_files, file_extractor = file_extractor).load_data()

if not documents:
    print("No documents were parsed")
else:
    print(f"Parsed {len(documents)} documents")
output_folder = "/home/binit/HistoryOfNepal/parsed_books/"
os.makedirs(output_folder, exist_ok= True)

concatenated_file_path = os.path.join(output_folder, "parsed_documents.md")
concatenated_content = ""
for i, document in enumerate(documents):
    concatenated_content += f"######## Document {i + 1} \n\n"
    concatenated_content += document.text + "\n\n"
try:
    with open(concatenated_file_path, "a") as f:
        f.write(concatenated_content)
    print(f"All documents have been concatenated and saved to {concatenated_file_path}")
except Exception as e:
    print(f"Error saving concatenated file: {e}")

