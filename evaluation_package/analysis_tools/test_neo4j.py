#!/usr/bin/env python3
"""Test Neo4j connection and analyze database contents"""
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

def analyze_neo4j_database():
    """Comprehensive analysis of Neo4j database contents"""
    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = "7P9fYDVO-vBVQxV6Ppeta2bfrTSwxmcfglZIryDb8vA"
    
    print("\n" + "="*80)
    print("NEO4J DATABASE COMPREHENSIVE ANALYSIS")
    print("="*80)
    
    try:
        driver = GraphDatabase.driver(url, auth=(username, password))
        
        with driver.session() as session:
            # 1. Overall database statistics
            print("\n📊 OVERALL DATABASE STATISTICS:")
            print("-" * 50)
            
            # Total nodes
            result = session.run("MATCH (n) RETURN count(n) as total_nodes")
            total_nodes = result.single()['total_nodes']
            print(f"Total Nodes: {total_nodes}")
            
            # Total relationships
            result = session.run("MATCH ()-[r]->() RETURN count(r) as total_relationships")
            total_relationships = result.single()['total_relationships']
            print(f"Total Relationships: {total_relationships}")
            
            # 2. Node analysis by labels
            print("\n📈 NODE ANALYSIS BY LABELS:")
            print("-" * 50)
            result = session.run("MATCH (n) RETURN labels(n) as labels, count(n) as count ORDER BY count DESC")
            for record in result:
                labels = record['labels']
                count = record['count']
                print(f"   {labels}: {count}")
            
            # 3. Relationship analysis by type
            print("\n🔗 RELATIONSHIP ANALYSIS BY TYPE:")
            print("-" * 50)
            result = session.run("MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as count ORDER BY count DESC LIMIT 20")
            for record in result:
                rel_type = record['rel_type']
                count = record['count']
                print(f"   {rel_type}: {count}")
            
            # 4. Document source analysis
            print("\n📋 DOCUMENT SOURCE ANALYSIS:")
            print("-" * 50)
            result = session.run("MATCH (n) WHERE n.source IS NOT NULL RETURN n.source as source, count(n) as count ORDER BY count DESC")
            for record in result:
                source = record['source']
                count = record['count']
                print(f"   {source}: {count}")
            
            # 5. OpenROAD-specific content analysis
            print("\n🔍 OPENROAD-SPECIFIC CONTENT:")
            print("-" * 50)
            
            # Search for OpenROAD-related nodes
            openroad_terms = ['openroad', 'vlsi', 'floorplan', 'placement', 'routing', 'timing', 'liberty', 'lef', 'def', 'verilog']
            for term in openroad_terms:
                result = session.run(f"MATCH (n) WHERE toLower(n.id) CONTAINS toLower('{term}') RETURN count(n) as count")
                count = result.single()['count']
                if count > 0:
                    print(f"   Nodes containing '{term}': {count}")
            
            # 6. Session1-specific patterns
            print("\n🎯 SESSION1 TUTORIAL PATTERNS:")
            print("-" * 50)
            session1_patterns = [
                'initFloorplan', 'getBlock', 'setSpecial', 'globalConnect',
                'getFloorplan', 'addGlobalConnect', 'getTritonCts', 'getReplace',
                'getGlobalRouter', 'getTritonRoute', 'getOpendp'
            ]
            
            for pattern in session1_patterns:
                result = session.run(f"MATCH (n) WHERE toLower(n.id) CONTAINS toLower('{pattern}') RETURN count(n) as count")
                count = result.single()['count']
                if count > 0:
                    print(f"   ✅ Found '{pattern}': {count} nodes")
                else:
                    print(f"   ❌ Missing '{pattern}': 0 nodes")
            
            # 7. Sample high-degree nodes (most connected)
            print("\n🌟 MOST CONNECTED NODES (Top 10):")
            print("-" * 50)
            result = session.run("""
                MATCH (n)
                OPTIONAL MATCH (n)-[r]-()
                WITH n, count(r) as degree
                WHERE degree > 0
                RETURN n.id as node_id, degree
                ORDER BY degree DESC
                LIMIT 10
            """)
            for record in result:
                node_id = record['node_id']
                degree = record['degree']
                print(f"   {node_id}: {degree} connections")
            
            # 8. Sample nodes with content
            print("\n📄 SAMPLE NODES WITH CONTENT:")
            print("-" * 50)
            result = session.run("MATCH (n) WHERE n.content IS NOT NULL RETURN n.id as id, n.content as content LIMIT 5")
            for i, record in enumerate(result, 1):
                node_id = record['id']
                content = record['content']
                content_preview = content[:100] + "..." if len(content) > 100 else content
                print(f"   {i}. {node_id}: {content_preview}")
            
            # 9. Relationship patterns analysis
            print("\n🔄 RELATIONSHIP PATTERNS:")
            print("-" * 50)
            result = session.run("""
                MATCH (a)-[r]->(b)
                RETURN a.id as source, type(r) as relationship, b.id as target
                LIMIT 10
            """)
            for record in result:
                source = record['source']
                relationship = record['relationship']
                target = record['target']
                print(f"   {source} --{relationship}--> {target}")
            
            # 10. Check for file-based content
            print("\n📁 FILE-BASED CONTENT ANALYSIS:")
            print("-" * 50)
            file_extensions = ['.py', '.md', '.txt', '.csv', '.json']
            for ext in file_extensions:
                result = session.run(f"MATCH (n) WHERE toLower(n.id) CONTAINS '{ext}' RETURN count(n) as count")
                count = result.single()['count']
                if count > 0:
                    print(f"   Nodes related to {ext} files: {count}")
            
        driver.close()
        
    except Exception as e:
        print(f"❌ Error analyzing Neo4j database: {e}")

def main():
    """Main function to test connection and analyze database"""
    print("🔍 NEO4J CONNECTION TEST AND DATABASE ANALYSIS")
    
    # Test basic connection
    if test_neo4j_connection():
        # Perform comprehensive analysis
        analyze_neo4j_database()
    else:
        print("❌ Cannot proceed with analysis due to connection failure")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main() 