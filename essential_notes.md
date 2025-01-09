store data in new_books 
and later shift to documents to books folders. 
first. We will run parse.py 
then we will run extraction.py
then we will hybrid_search and neo4j_graph which will embed the data and then store in qdrant and knowledge graph
and finally we will be custom_agents.py



to access neo4j


use bolt localhost:7687

when there is neo4j websocket issue . then we need to go to neo4j container and then go to config . and then run apt-get update && apt-get install nano -y
 and then then go inside nano neo4j.conf then go to network config and then uncomment server.default_listen_address=0.0.0.0



 IN NEO4J.
 **Delete All Nodes and Relationships**
 MATCH (n) DETACH DELETE n;

 **SHOW INDEX**
SHOW INDEXES;

 **DROP INDEX** 
DROP INDEX `index_name`;
