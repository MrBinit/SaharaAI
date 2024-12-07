from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
import os
from dotenv import load_dotenv
from langchain.schema import Document
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()

# Environment variables for Neo4j connection
url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
chunked_folder_path = os.getenv("CHUNK_FOLDER_PATH")  # Folder with text chunks

# Initialize Neo4j driver
driver = GraphDatabase.driver(url, auth=(username, password))

# Function to read documents from a folder (text chunks)
def read_documents(chunked_folder_path):
    docs = []
    try:
        for filename in os.listdir(chunked_folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(chunked_folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    docs.append(Document(page_content=content, metadata={}))
    except Exception as e:
        print(f"Error reading documents from folder: {e}")
    return docs

# Initialize the embedding model
try:
    embedding_model = OllamaEmbeddings(model="mxbai-embed-large")
    print("Embedding model initialized successfully.")
except Exception as e:
    print(f"Error initializing the embedding model: {e}")
    exit(1)

# Read documents from the specified folder
docs = read_documents(chunked_folder_path)

if not docs:
    print("No documents were loaded. Exiting the process.")
    exit(1)

# Create historical data in Neo4j (Historical events and figures)
def create_historical_data():
    with driver.session() as session:
        # Create nodes for multiple people, events, and locations
        session.run("""
        // Historical figures
        MERGE (p1:Person {name: "Prithvi Narayan Shah"})
        MERGE (p2:Person {name: "Tribhuvan Bir Bikram Shah"})
        MERGE (p3:Person {name: "Birendra Bir Bikram Shah"})
        MERGE (p4:Person {name: "Bishweshwar Prasad Koirala"})

        // Locations
        MERGE (gorkha:Location {name: "Gorkha"})
        MERGE (kathmandu:Location {name: "Kathmandu"})
        MERGE (patan:Location {name: "Patan"})

        // Events
        MERGE (unification:Event {name: "Unification of Nepal", year: 1768})
        MERGE (revolution:Event {name: "1951 Revolution", year: 1951})
        MERGE (democracy:Event {name: "Democracy Movement of 1990", year: 1990})
        MERGE (maoist:Event {name: "Maoist Insurgency", year: 1996})

        // Create relationships
        MERGE (p1)-[:LED]->(unification)
        MERGE (p2)-[:LED]->(revolution)
        MERGE (p3)-[:LED]->(democracy)
        MERGE (p4)-[:PARTICIPATED_IN]->(maoist)

        MERGE (p1)-[:BORN_IN]->(gorkha)
        MERGE (p2)-[:BORN_IN]->(gorkha)
        MERGE (p3)-[:BORN_IN]->(kathmandu)
        MERGE (p4)-[:BORN_IN]->(patan)

        MERGE (unification)-[:HAPPENED_IN]->(kathmandu)
        MERGE (revolution)-[:HAPPENED_IN]->(kathmandu)
        MERGE (democracy)-[:HAPPENED_IN]->(kathmandu)
        MERGE (maoist)-[:HAPPENED_IN]->(kathmandu)
        """)

# Create historical data in Neo4j
create_historical_data()

# Initialize the vector store and store the embedded documents in Neo4j
try:
    vectorstore = Neo4jVector.from_documents(
        embedding=embedding_model,
        documents=docs,
        url=url,
        username=username,
        password=password,
        distance_strategy='COSINE'
    )
    print("Documents successfully embedded and stored in Neo4j.")
except Exception as e:
    print(f"Error storing documents in Neo4j: {e}")
    exit(1)

# Query the vector store (e.g., for "Unification of Nepal")
query = "Tell me about the unification of Nepal"
results = vectorstore.query(query)

# Display the results from the semantic search
print(f"Query results for '{query}':")
for result in results:
    print(result)

# Example of querying Neo4j directly to retrieve historical data
def get_historical_figures_in_event(event_name):
    with driver.session() as session:
        result = session.run("""
        MATCH (p:Person)-[:LED]->(e:Event)
        WHERE e.name = $event_name
        RETURN p.name AS person_name
        """, event_name=event_name)
        
        return [record["person_name"] for record in result]

# Query historical figures who participated in the "Unification of Nepal"
historical_figures = get_historical_figures_in_event("Unification of Nepal")
print(f"Historical figures in the Unification of Nepal: {historical_figures}")

# Query events that happened in Kathmandu
def get_events_in_location(location_name):
    with driver.session() as session:
        result = session.run("""
        MATCH (e:Event)-[:HAPPENED_IN]->(l:Location)
        WHERE l.name = $location_name
        RETURN e.name AS event_name, e.year AS event_year
        """, location_name=location_name)
        
        return [(record["event_name"], record["event_year"]) for record in result]

# Query events that happened in Kathmandu
events_in_kathmandu = get_events_in_location("Kathmandu")
print(f"Events that happened in Kathmandu: {events_in_kathmandu}")
