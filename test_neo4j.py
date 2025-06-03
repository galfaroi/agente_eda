#!/usr/bin/env python3
"""Test Neo4j connection independently"""
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

def test_neo4j_connection():
    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = "7P9fYDVO-vBVQxV6Ppeta2bfrTSwxmcfglZIryDb8vA"   #os.getenv("NEO4J_PASSWORD")
    
    print(f"Testing connection to: {url}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password) if password else 'None'}")
    
    try:
        driver = GraphDatabase.driver(url, auth=(username, password))
        
        # Test the connection
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j' as message")
            record = result.single()
            print(f"✅ Connection successful: {record['message']}")
            
            # Check database info
            result = session.run("CALL db.info()")
            info = result.single()
            print(f"Database: {info}")
            
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_neo4j_connection() 