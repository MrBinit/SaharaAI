from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# Initialize Neo4j connection
driver = GraphDatabase.driver(url, auth=(username, password))

def check_connection():
    try:
        with driver.session() as session:
            session.run("RETURN 1 AS test")
            print("Database connection is successful!")
    except Exception as e:
        print(f"Error connecting to Neo4j: {e}")

check_connection()
