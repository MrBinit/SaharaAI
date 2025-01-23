# this  code will execute neo4j script and create graph database
from retrievers.neo4j_graph import query_similarity_search


if __name__ == "__main__":
    query = "Who is King Birendra"
    query_similarity_search(query)

