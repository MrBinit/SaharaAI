from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Neo4j credentials from the environment variables
url = os.getenv("NEO4J_URL")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# Create a connection to the Neo4j database
driver = GraphDatabase.driver(url, auth=(username, password))

# Define the query function to run a query on Neo4j and return the results
def query_neo4j(query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()  # Fetch all results at once

# Step 1: Check if there are any 'Chunk' nodes in the database and inspect their properties
query_check_chunk_properties = """
MATCH (c:Chunk) RETURN c LIMIT 10
"""

# Run the query to check for 'Chunk' nodes and inspect properties
result_check_properties = query_neo4j(query_check_chunk_properties)

print("Checking 'Chunk' nodes for properties:")
if result_check_properties:
    for record in result_check_properties:
        print(record)
else:
    print("\nNo 'Chunk' nodes found.")

# Step 2: Search for content in the 'Chunk' nodes (adjusted for the right property name)
# You can change `page_content` to the actual property name if different.
query_search_content = """
MATCH (c:Chunk) WHERE c.page_content CONTAINS 'Nepal'
RETURN c.page_content LIMIT 10
"""

result_search = query_neo4j(query_search_content)

print("\nSearching for content containing 'Nepal' in 'Chunk' nodes:")
if result_search:
    for record in result_search:
        print(f"Page Content: {record['page_content']}")
else:
    print("No content containing 'Nepal' found.")
