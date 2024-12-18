from graph import retrieval_from_graph

query = "who is king prithvi narayan?"
vector_results = retrieval_from_graph.similarity_search(query, k=2)
for doc, score in vector_results:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)

