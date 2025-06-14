#!/usr/bin/env python3
"""
Ingest RAGAPIs.csv into both vector database (Qdrant) and Neo4j graph database
"""

import os
import csv
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any

from camel.embeddings import OpenAIEmbedding
from camel.types import EmbeddingModelType
from camel.storages import QdrantStorage, Neo4jGraph
from camel.loaders import UnstructuredIO
from camel.agents import KnowledgeGraphAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig

def load_rag_apis_csv(file_path: str) -> List[Dict[str, Any]]:
    """Load and parse the RAGAPIs.csv file"""
    print(f"📖 Loading RAGAPIs.csv from: {file_path}")
    
    apis = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            # Clean up the data
            api_entry = {
                'id': f"api_{i}",
                'description': row.get('Description:', '').strip(),
                'function_name': row.get('Function Name:', '').strip(),
                'parameters': row.get('Parameters:', '').strip(),
                'return_type': row.get('Return Type:', '').strip(),
                'source': 'RAGAPIs.csv'
            }
            
            # Create content for vector embedding
            content_parts = []
            if api_entry['description']:
                content_parts.append(f"Description: {api_entry['description']}")
            if api_entry['function_name']:
                content_parts.append(f"Function: {api_entry['function_name']}")
            if api_entry['parameters']:
                content_parts.append(f"Parameters: {api_entry['parameters']}")
            if api_entry['return_type']:
                content_parts.append(f"Returns: {api_entry['return_type']}")
            
            api_entry['content'] = ' | '.join(content_parts)
            
            if api_entry['content'].strip():  # Only add non-empty entries
                apis.append(api_entry)
    
    print(f"✅ Loaded {len(apis)} API entries from RAGAPIs.csv")
    return apis

def ingest_to_vector_database(apis: List[Dict[str, Any]]):
    """Ingest API data into Qdrant vector database"""
    print("\n📊 INGESTING INTO VECTOR DATABASE (QDRANT)")
    print("=" * 60)
    
    try:
        # Initialize embedding model
        embedding = OpenAIEmbedding(model_type=EmbeddingModelType.TEXT_EMBEDDING_3_LARGE)
        
        # Initialize vector store
        vector_store = QdrantStorage(
            vector_dim=embedding.get_output_dim(),
            path="vector_db/",
            collection_name="documents_collection",
        )
        
        print(f"🔧 Adding {len(apis)} API entries to vector database...")
        
        # Prepare documents for ingestion
        documents = []
        for api in apis:
            doc = {
                'content': api['content'],
                'metadata': {
                    'source': api['source'],
                    'function_name': api['function_name'],
                    'description': api['description'],
                    'return_type': api['return_type'],
                    'type': 'openroad_api'
                }
            }
            documents.append(doc)
        
        # Add documents to vector store
        for i, doc in enumerate(documents):
            try:
                # Create embedding
                embedding_vector = embedding.embed_list([doc['content']])[0]
                
                # Add to vector store
                vector_store.add(
                    payload={
                        'content': doc['content'],
                        'metadata': doc['metadata'],
                        'source': doc['metadata']['source']
                    },
                    vector=embedding_vector,
                    id=f"api_{i+1}"
                )
                
                if (i + 1) % 20 == 0:
                    print(f"   Added {i+1}/{len(documents)} documents...")
                    
            except Exception as e:
                print(f"   ⚠️ Error adding document {i+1}: {e}")
        
        print(f"✅ Successfully added {len(documents)} API entries to vector database")
        
    except Exception as e:
        print(f"❌ Error ingesting to vector database: {e}")

def ingest_to_neo4j_database(apis: List[Dict[str, Any]]):
    """Ingest API data into Neo4j graph database"""
    print("\n🔗 INGESTING INTO NEO4J GRAPH DATABASE")
    print("=" * 60)
    
    try:
        # Initialize Neo4j connection
        n4j = Neo4jGraph(
            url="neo4j+s://a77d863c.databases.neo4j.io",
            username="neo4j",
            password="f1zopPMnKXlhQAYvugcoLUr8t0s9QruIyYsY0YxBBhU"
        )
        
        # Initialize models for KG agent
        try:
            chat_cfg = ChatGPTConfig(temperature=0.2).as_dict()
        except:
            chat_cfg = {'temperature': 0.2}
        
        openai_model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4_1,
            model_config_dict=chat_cfg,
        )
        
        # Initialize KG agent
        kg_agent = KnowledgeGraphAgent(model=openai_model)
        uio = UnstructuredIO()
        
        print(f"🔧 Processing {len(apis)} API entries for knowledge graph...")
        
        # Process APIs in batches
        batch_size = 10
        for i in range(0, len(apis), batch_size):
            batch = apis[i:i+batch_size]
            
            # Create batch content for KG extraction
            batch_content = []
            for api in batch:
                api_text = f"""
OpenROAD API Function: {api['function_name']}
Description: {api['description']}
Parameters: {api['parameters']}
Return Type: {api['return_type']}
Source: {api['source']}
"""
                batch_content.append(api_text.strip())
            
            combined_content = "\n\n".join(batch_content)
            
            try:
                # Create element for KG processing
                element = uio.create_element_from_text(
                    text=combined_content,
                    element_id=f"rag_apis_batch_{i//batch_size + 1}"
                )
                
                # Extract knowledge graph elements
                kg_element = kg_agent.run(element, parse_graph_elements=True)
                
                # Add nodes to Neo4j
                for node in kg_element.nodes:
                    try:
                        # Create node with properties
                        cypher = """
                        MERGE (n {id: $node_id})
                        SET n.source = $source,
                            n.type = $node_type,
                            n.batch = $batch_id
                        """
                        n4j.query(
                            query=cypher,
                            parameters={
                                'node_id': node.id,
                                'source': 'RAGAPIs.csv',
                                'node_type': 'openroad_api',
                                'batch_id': f"batch_{i//batch_size + 1}"
                            }
                        )
                    except Exception as e:
                        print(f"   ⚠️ Error adding node {node.id}: {e}")
                
                # Add relationships to Neo4j
                for edge in kg_element.edges:
                    try:
                        cypher = """
                        MATCH (a {id: $source_id}), (b {id: $target_id})
                        MERGE (a)-[r:RELATES_TO]->(b)
                        SET r.relationship_type = $rel_type,
                            r.source = $source
                        """
                        n4j.query(
                            query=cypher,
                            parameters={
                                'source_id': edge.source_node_id,
                                'target_id': edge.target_node_id,
                                'rel_type': edge.edge_type,
                                'source': 'RAGAPIs.csv'
                            }
                        )
                    except Exception as e:
                        print(f"   ⚠️ Error adding relationship: {e}")
                
                print(f"   Processed batch {i//batch_size + 1}/{(len(apis) + batch_size - 1)//batch_size}")
                
            except Exception as e:
                print(f"   ⚠️ Error processing batch {i//batch_size + 1}: {e}")
        
        # Add specific OpenROAD API nodes for important functions
        print("🔧 Adding specific OpenROAD API function nodes...")
        
        important_functions = [
            'initFloorplan', 'getBlock', 'setSpecial', 'globalConnect',
            'getFloorplan', 'addGlobalConnect', 'getTritonCts', 'getReplace',
            'getGlobalRouter', 'getTritonRoute', 'getOpendp', 'readLiberty',
            'readLef', 'readVerilog', 'readDef', 'link'
        ]
        
        for func in important_functions:
            # Find APIs that contain this function
            matching_apis = [api for api in apis if func.lower() in api['function_name'].lower()]
            
            if matching_apis:
                for api in matching_apis:
                    try:
                        cypher = """
                        MERGE (f:OpenROADFunction {id: $func_id})
                        SET f.function_name = $func_name,
                            f.description = $description,
                            f.parameters = $parameters,
                            f.return_type = $return_type,
                            f.source = $source,
                            f.type = 'openroad_function'
                        """
                        n4j.query(
                            query=cypher,
                            parameters={
                                'func_id': func,
                                'func_name': api['function_name'],
                                'description': api['description'],
                                'parameters': api['parameters'],
                                'return_type': api['return_type'],
                                'source': 'RAGAPIs.csv'
                            }
                        )
                    except Exception as e:
                        print(f"   ⚠️ Error adding function node {func}: {e}")
        
        print(f"✅ Successfully processed API data for Neo4j graph database")
        
    except Exception as e:
        print(f"❌ Error ingesting to Neo4j database: {e}")

def verify_ingestion():
    """Verify that the data was successfully ingested"""
    print("\n🔍 VERIFYING INGESTION")
    print("=" * 60)
    
    # Check vector database
    try:
        embedding = OpenAIEmbedding(model_type=EmbeddingModelType.TEXT_EMBEDDING_3_LARGE)
        vector_store = QdrantStorage(
            vector_dim=embedding.get_output_dim(),
            path="vector_db/",
            collection_name="documents_collection",
        )
        
        collection_info = vector_store.client.get_collection("documents_collection")
        print(f"📊 Vector Database: {collection_info.points_count} total points")
        
        # Search for API-related content
        test_query = "openroad initFloorplan"
        results = vector_store.query(query=test_query, top_k=3)
        print(f"📋 Sample search for '{test_query}': Found {len(results)} results")
        
    except Exception as e:
        print(f"❌ Error verifying vector database: {e}")
    
    # Check Neo4j database
    try:
        n4j = Neo4jGraph(
            url="neo4j+s://a77d863c.databases.neo4j.io",
            username="neo4j",
            password="f1zopPMnKXlhQAYvugcoLUr8t0s9QruIyYsY0YxBBhU"
        )
        
        # Count nodes from RAGAPIs.csv
        result = n4j.query("MATCH (n) WHERE n.source = 'RAGAPIs.csv' RETURN count(n) as count")
        api_nodes = result[0]['count'] if result else 0
        print(f"🔗 Neo4j Database: {api_nodes} nodes from RAGAPIs.csv")
        
        # Check for specific function nodes
        result = n4j.query("MATCH (n:OpenROADFunction) RETURN count(n) as count")
        func_nodes = result[0]['count'] if result else 0
        print(f"🔧 Neo4j Database: {func_nodes} OpenROAD function nodes")
        
    except Exception as e:
        print(f"❌ Error verifying Neo4j database: {e}")

def main():
    """Main ingestion function"""
    load_dotenv()
    
    print("🚀 INGESTING RAGAPIs.csv INTO RAG DATABASES")
    print("=" * 80)
    
    # Check if file exists
    csv_file = "RAGAPIs.csv"
    if not Path(csv_file).exists():
        print(f"❌ File not found: {csv_file}")
        return
    
    # Load API data
    apis = load_rag_apis_csv(csv_file)
    
    if not apis:
        print("❌ No API data loaded")
        return
    
    # Ingest into both databases
    ingest_to_vector_database(apis)
    ingest_to_neo4j_database(apis)
    
    # Verify ingestion
    verify_ingestion()
    
    print("\n" + "=" * 80)
    print("✅ INGESTION COMPLETE")
    print("=" * 80)
    print(f"📊 Total API entries processed: {len(apis)}")
    print("🎯 The RAG system now has access to OpenROAD API documentation!")

if __name__ == "__main__":
    main() 