from hybrid import retrieve_documents_from_qdrant

# Query to retrieve documents based on the search query
query = "How was King birendra?"

# Retrieve documents from Qdrant
docs_with_score = retrieve_documents_from_qdrant(query)

print("meow", docs_with_score)