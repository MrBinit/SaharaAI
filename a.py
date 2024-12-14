from hybrid import retrieve_documents_from_qdrant

# Query to retrieve documents based on the search query
query = "Points of sugauli treaty"

# Retrieve documents from Qdrant
docs_with_score = retrieve_documents_from_qdrant(query)



# Print the retrieved documents
if docs_with_score:
    print(f"Results for the query '{query}':")
    for result in docs_with_score:
        print("-" * 80)
        print("Score:", result["score"])
        print(result["content"])
        print("-" * 80)
else:
    print("No results found for the query.")