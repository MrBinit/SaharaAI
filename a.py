from neo4j import GraphDatabase

uri = "bolt://neo4j_database:7687"
username = "neo4j"
password = "neo4j_admin"

driver = GraphDatabase.driver(uri, auth=(username, password))

def push_data(tx):
    # Create historical figures as nodes
    tx.run("""
        CREATE (mahendra:Person {name: 'King Mahendra', role: 'King of Nepal', reign: '1955-1972'})
        CREATE (rana_regime:Event {name: 'Rana Regime', description: 'Autocratic rule by the Rana family in Nepal', period: '1846-1951'})
        CREATE (tribhuvan:Person {name: 'King Tribhuvan', role: 'King of Nepal', reign: '1911-1955'})
        CREATE (prithvi:Person {name: 'King Prithvi Narayan Shah', role: 'Founder of Unified Nepal', reign: '1743-1775'})
        CREATE (bp_koirala:Person {name: 'BP Koirala', role: 'First Democratically Elected Prime Minister of Nepal', term: '1959-1960'})
        CREATE (military_coup:Event {name: '1960 Military Coup', description: 'King Mahendra’s coup that dissolved the democratic government', year: 1960})
    """)

    # Create relationships
    tx.run("""
        MATCH (mahendra:Person {name: 'King Mahendra'}),
              (tribhuvan:Person {name: 'King Tribhuvan'}),
              (rana_regime:Event {name: 'Rana Regime'}),
              (prithvi:Person {name: 'King Prithvi Narayan Shah'}),
              (bp_koirala:Person {name: 'BP Koirala'}),
              (military_coup:Event {name: '1960 Military Coup'})
        CREATE (tribhuvan)-[:ENDED]->(rana_regime)
        CREATE (mahendra)-[:CONDUCTED]->(military_coup)
        CREATE (bp_koirala)-[:OVERTHROWN_BY]->(military_coup)
        CREATE (prithvi)-[:FOUNDED]->(:Entity {name: 'Unified Nepal'})
        CREATE (mahendra)-[:SUCCEEDED]->(tribhuvan)
    """)

try:
    with driver.session() as session:
        session.execute_write(push_data)
        print("Data pushed successfully!")
        print(uri)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.close()


from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://172.20.0.3:7687", auth=("neo4j", "neo4j_admin"))
with driver.session() as session:
    session.run("RETURN 1")
    print("Connected successfully")
