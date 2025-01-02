from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.schema import Document
from neo4j import GraphDatabase
import time

# Configuration
NEO4J_URI = "bolt://neo4j_database:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j_admin"
OLLAMA_BASE_URL = "http://ollama:11434"
VECTOR_DIMENSION = 1024  # Updated to match mxbai-embed-large dimension

def setup_neo4j_indexes():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            # Drop existing indexes first
            print("Dropping existing indexes...")
            session.run("DROP INDEX vector_index IF EXISTS")
            session.run("DROP INDEX document_content IF EXISTS")
            
            # Create vector index with correct dimensions
            print("Creating vector index...")
            session.run(f"""
                CREATE VECTOR INDEX vector_index IF NOT EXISTS
                FOR (n:Document)
                ON (n.embedding)
                OPTIONS {{indexConfig: {{
                    `vector.dimensions`: {VECTOR_DIMENSION},
                    `vector.similarity_function`: 'cosine'
                }}}}
            """)
            
            # Create text index
            print("Creating text index...")
            session.run("""
                CREATE TEXT INDEX document_content IF NOT EXISTS
                FOR (n:Document)
                ON (n.content)
            """)
            
            print("Indexes created successfully!")
            
            # Verify indexes
            result = session.run("SHOW INDEXES")
            print("\nAvailable indexes:")
            for record in result:
                print(record)
                
    except Exception as e:
        print(f"Error setting up indexes: {e}")
    finally:
        driver.close()

# Your documents
documents = [
    Document(page_content="King Birendra was the 11th King of Nepal.", metadata={"source": "history.txt"}),
    Document(page_content="King Prithvi Narayan Shah unified Nepal.", metadata={"source": "founder.txt"}),
]

def create_vectorstore(documents):
    try:
        # Initialize embedding model
        embedding_model = OllamaEmbeddings(
            model="mxbai-embed-large",
            base_url=OLLAMA_BASE_URL
        )
        print("Embedding model initialized successfully.")

        # Create vector store
        vectorstore = Neo4jVector.from_documents(
            embedding=embedding_model,
            documents=documents,
            url=NEO4J_URI,
            username=NEO4J_USER,
            password=NEO4J_PASSWORD,
            index_name="vector_index",
            keyword_index_name="document_content",
            node_label="Document",
            embedding_node_property="embedding",
            text_node_property="content"
        )
        print("Vector store created successfully!")
        return vectorstore
    except Exception as e:
        print(f"Error creating vector store: {e}")
        import traceback
        print("\nFull error traceback:")
        print(traceback.format_exc())
        return None

def perform_similarity_search(query):
    vectorstore = create_vectorstore(documents)
    if vectorstore:
        try:
            print(f"\nPerforming similarity search for: '{query}'")
            results = vectorstore.similarity_search_with_score(query, k=2)
            for doc, score in results:
                print(f"\nDocument: {doc.page_content}")
                print(f"Score: {score}")
        except Exception as e:
            print(f"Error during similarity search: {e}")

def clean_database():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            # Remove all Document nodes
            session.run("MATCH (n:Document) DETACH DELETE n")
            print("Cleaned up existing Document nodes")
    except Exception as e:
        print(f"Error cleaning database: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    # Clean up existing data first
    clean_database()
    
    # Setup indexes with correct dimensions
    setup_neo4j_indexes()
    
    # Wait a moment for indexes to be ready
    print("\nWaiting for indexes to be ready...")
    time.sleep(5)
    
    # Perform the search
    query = "Who unified Nepal?"
    perform_similarity_search(query)