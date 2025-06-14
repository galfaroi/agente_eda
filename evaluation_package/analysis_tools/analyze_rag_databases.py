#!/usr/bin/env python3
"""
Analyze the contents of the RAG system databases:
1. Vector database (Qdrant) - what documents are stored
2. Neo4j graph database - what nodes and relationships exist
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from camel.storages import QdrantStorage, Neo4jGraph
from camel.embeddings import OpenAIEmbedding
from camel.types import EmbeddingModelType

def analyze_vector_database():
    """Analyze the Qdrant vector database contents"""
    print("="*80)
    print("VECTOR DATABASE (QDRANT) ANALYSIS")
    print("="*80)
    
    try:
        # Initialize embedding model (same as pipeline)
        embedding = OpenAIEmbedding(model_type=EmbeddingModelType.TEXT_EMBEDDING_3_LARGE)
        
        # Initialize vector store
        vector_store = QdrantStorage(
            vector_dim=embedding.get_output_dim(),
            path="vector_db/",
            collection_name="documents_collection",
        )
        
        # Get collection info
        collection_info = vector_store.client.get_collection("documents_collection")
        print(f"📊 Collection: {collection_info.config.params}")
        print(f"📈 Vector count: {collection_info.points_count}")
        print(f"📏 Vector dimension: {collection_info.config.params.vectors.size}")
        
        # Get some sample points
        print(f"\n📋 Sample documents in vector database:")
        points = vector_store.client.scroll(
            collection_name="documents_collection",
            limit=20,
            with_payload=True,
            with_vectors=False
        )[0]
        
        for i, point in enumerate(points, 1):
            payload = point.payload
            print(f"\n{i}. Point ID: {point.id}")
            if 'content' in payload:
                content_preview = payload['content'][:200] + "..." if len(payload['content']) > 200 else payload['content']
                print(f"   Content: {content_preview}")
            if 'metadata' in payload:
                print(f"   Metadata: {payload['metadata']}")
            if 'source' in payload:
                print(f"   Source: {payload['source']}")
                
    except Exception as e:
        print(f"❌ Error analyzing vector database: {e}")
        print("   This might mean the vector database is empty or not initialized")

def analyze_neo4j_database():
    """Analyze the Neo4j graph database contents"""
    print("\n" + "="*80)
    print("NEO4J GRAPH DATABASE ANALYSIS")
    print("="*80)
    
    try:
        # Initialize Neo4j connection (same as pipeline)
        n4j = Neo4jGraph(
            url="neo4j+s://a77d863c.databases.neo4j.io",
            username="neo4j",
            password="f1zopPMnKXlhQAYvugcoLUr8t0s9QruIyYsY0YxBBhU"
        )
        
        # Get database statistics
        print("📊 Database Statistics:")
        
        # Count nodes by label
        node_counts = n4j.query("MATCH (n) RETURN labels(n) as labels, count(n) as count")
        print(f"\n📈 Node counts by label:")
        for record in node_counts:
            labels = record['labels']
            count = record['count']
            print(f"   {labels}: {count}")
        
        # Count relationships by type
        rel_counts = n4j.query("MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as count")
        print(f"\n🔗 Relationship counts by type:")
        for record in rel_counts:
            rel_type = record['rel_type']
            count = record['count']
            print(f"   {rel_type}: {count}")
        
        # Sample nodes
        print(f"\n📋 Sample nodes (first 10):")
        sample_nodes = n4j.query("MATCH (n) RETURN n LIMIT 10")
        for i, record in enumerate(sample_nodes, 1):
            node = record['n']
            print(f"\n{i}. Node: {dict(node)}")
        
        # Sample relationships
        print(f"\n🔗 Sample relationships (first 10):")
        sample_rels = n4j.query("MATCH (a)-[r]->(b) RETURN a.id as source, type(r) as rel_type, b.id as target LIMIT 10")
        for i, record in enumerate(sample_rels, 1):
            source = record['source']
            rel_type = record['rel_type']
            target = record['target']
            print(f"{i}. {source} --{rel_type}--> {target}")
            
        # Look for OpenROAD-specific content
        print(f"\n🔍 OpenROAD-related nodes:")
        openroad_nodes = n4j.query("MATCH (n) WHERE toLower(n.id) CONTAINS 'openroad' OR toLower(n.id) CONTAINS 'vlsi' OR toLower(n.id) CONTAINS 'floorplan' RETURN n LIMIT 10")
        for i, record in enumerate(openroad_nodes, 1):
            node = record['n']
            print(f"{i}. {dict(node)}")
            
    except Exception as e:
        print(f"❌ Error analyzing Neo4j database: {e}")
        print("   This might mean the database is empty or connection failed")

def check_session1_ingestion():
    """Check if session1 files have been ingested"""
    print("\n" + "="*80)
    print("SESSION1 FILES INGESTION CHECK")
    print("="*80)
    
    session1_files = [
        "demo1_flow.py",
        "demo1_helpers.py", 
        "demo1_query.py",
        "demo2_IR.py",
        "demo2_IR_helpers.py",
        "demo2_gate_sizing.py",
        "demo2_gate_sizing_helpers.py",
        "README.md"
    ]
    
    try:
        # Check vector database for session1 content
        embedding = OpenAIEmbedding(model_type=EmbeddingModelType.TEXT_EMBEDDING_3_LARGE)
        vector_store = QdrantStorage(
            vector_dim=embedding.get_output_dim(),
            path="vector_db/",
            collection_name="documents_collection",
        )
        
        print("🔍 Searching for session1 files in vector database:")
        for filename in session1_files:
            # Search for content containing the filename
            points = vector_store.client.scroll(
                collection_name="documents_collection",
                scroll_filter={
                    "should": [
                        {"key": "source", "match": {"value": filename}},
                        {"key": "content", "match": {"text": filename}}
                    ]
                },
                limit=5,
                with_payload=True
            )[0]
            
            if points:
                print(f"   ✅ Found {len(points)} entries for {filename}")
                for point in points[:2]:  # Show first 2
                    if 'source' in point.payload:
                        print(f"      Source: {point.payload['source']}")
            else:
                print(f"   ❌ No entries found for {filename}")
                
    except Exception as e:
        print(f"❌ Error checking session1 ingestion: {e}")
    
    try:
        # Check Neo4j for session1 content
        n4j = Neo4jGraph(
            url="neo4j+s://a77d863c.databases.neo4j.io",
            username="neo4j",
            password="f1zopPMnKXlhQAYvugcoLUr8t0s9QruIyYsY0YxBBhU"
        )
        
        print(f"\n🔍 Searching for session1 content in Neo4j:")
        session1_terms = ["floorplan", "initFloorplan", "getBlock", "setSpecial", "globalConnect"]
        
        for term in session1_terms:
            nodes = n4j.query(f"MATCH (n) WHERE toLower(n.id) CONTAINS toLower('{term}') RETURN n LIMIT 3")
            if nodes:
                print(f"   ✅ Found {len(nodes)} nodes related to '{term}'")
                for record in nodes:
                    node = record['n']
                    print(f"      Node: {node.get('id', 'No ID')}")
            else:
                print(f"   ❌ No nodes found for '{term}'")
                
    except Exception as e:
        print(f"❌ Error checking Neo4j for session1 content: {e}")

def main():
    """Main analysis function"""
    load_dotenv()
    
    print("🔍 ANALYZING RAG SYSTEM DATABASES")
    print("This will help understand what knowledge is available to the agent")
    
    # Analyze vector database
    analyze_vector_database()
    
    # Analyze Neo4j database  
    analyze_neo4j_database()
    
    # Check session1 ingestion
    check_session1_ingestion()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main() 