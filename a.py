from langchain_ollama import OllamaEmbeddings

# Initialize the embedding model
embedding_model = OllamaEmbeddings(model="mxbai-embed-large")

# Sample text for embedding
sample_text = "This is a test sentence for embedding."

# Embed the sample text using the appropriate method
embedding_result = embedding_model.embed_documents([sample_text])

# Check if the embedding result is valid (non-empty)
if embedding_result and len(embedding_result[0]) > 0:
    print("Embedding was successful!")
    print("Embedding: ", embedding_result[0])
else:
    print("Embedding failed or returned an empty result.")
