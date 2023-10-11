from neo4j import GraphDatabase
import os

URI = os.getenv('NEO4J_URI')
AUTH = (os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))


drive = None
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    drive = driver