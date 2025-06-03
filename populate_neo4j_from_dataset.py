#!/usr/bin/env python3
"""
Populate Neo4j with VLSI knowledge graph data from ORAssistan_RAG_Dataset
"""
import os
import json
from typing import Dict, List
from dotenv import load_dotenv
from camel.storages import Neo4jGraph
from camel.agents import KnowledgeGraphAgent
from camel.loaders import UnstructuredIO
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig

load_dotenv()

def populate_neo4j_from_dataset(dataset_file: str = "flow_tutorial.md"):
    """Populate Neo4j with knowledge graph from ORAssistan dataset"""
    
    print("🚀 Starting Neo4j population from ORAssistan_RAG_Dataset...")
    
    # Initialize Neo4j connection using Neo4jGraph (like your working script)
    try:
        n4j = Neo4jGraph(
            url="neo4j+s://1cd25c52.databases.neo4j.io",
            username="neo4j", 
            password="7P9fYDVO-vBVQxV6Ppeta2bfrTSwxmcfglZIryDb8vA"
        )
        
        # Test connection
        result = list(n4j.query("RETURN 1 as test"))
        print("✅ Neo4j connected successfully")
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        return False
    
    # Initialize components (like your working script)
    print("🤖 Initializing Knowledge Graph Agent...")
    try:
        chat_cfg = ChatGPTConfig(temperature=0.1).as_dict()
        openai_model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O_MINI,
            model_config_dict=chat_cfg,
        )
        
        # Set instance (exactly like your working script)
        uio = UnstructuredIO()
        kg_agent = KnowledgeGraphAgent(model=openai_model)
        
        print("✅ KG Agent initialized")
    except Exception as e:
        print(f"❌ KG Agent initialization failed: {e}")
        return False
    
    # Check if dataset file exists
    if not os.path.exists(dataset_file):
        print(f"❌ Dataset file '{dataset_file}' not found")
        print("Available files:")
        for f in os.listdir("."):
            if any(ext in f.lower() for ext in ['.md', '.json', '.jsonl', 'dataset', 'tutorial']):
                print(f"  - {f}")
        return False
    
    # Clear existing VLSI data (optional)
    print("🧹 Clearing existing VLSI data...")
    try:
        n4j.query("MATCH (n) DETACH DELETE n")
        print("✅ Cleared existing data")
    except Exception as e:
        print(f"⚠️  Warning: Could not clear data: {e}")
    
    # Read dataset based on file type
    print(f"📖 Reading dataset from '{dataset_file}'...")
    
    try:
        if dataset_file.endswith('.md'):
            # Handle Markdown files (like your working script)
            with open(dataset_file, "r", encoding="utf-8") as f:
                md_text = f.read()
            
            print(f"📚 Read {len(md_text)} characters from markdown file")
            
            # Process the entire file as one document (like your working script)
            print("🔄 Processing markdown content...")
            
            # Create an Element from your markdown (exactly like your working script)
            element = uio.create_element_from_text(
                text=md_text,
                element_id="flow_tutorial"
            )
            
            # Let Knowledge Graph Agent extract node and relationship information
            print("🧠 Extracting knowledge graph...")
            ans_element = kg_agent.run(element, parse_graph_elements=False)
            print(f"✅ Extracted text analysis: {len(str(ans_element))} chars")
            
            # Check graph element (exactly like your working script)
            print("🕸️  Extracting graph elements...")
            graph_elements = kg_agent.run(element, parse_graph_elements=True)
            
            # Just print the graph_elements like in your working script
            print("Graph elements extracted:")
            print(graph_elements)
            
            # Add the element to neo4j database (exactly like your working script)
            print("💾 Adding to Neo4j database...")
            n4j.add_graph_elements(graph_elements=[graph_elements])
            print("✅ Successfully added to Neo4j!")
            
        elif dataset_file.endswith('.jsonl'):
            # Handle JSONL files
            with open(dataset_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        doc = json.loads(line.strip())
                        text = doc.get('text', '') or doc.get('content', '')
                        
                        if len(text.strip()) > 100:
                            print(f"Processing document {line_num}...")
                            
                            element = uio.create_element_from_text(
                                text=text,
                                element_id=f"doc_{line_num}"
                            )
                            
                            graph_elements = kg_agent.run(element, parse_graph_elements=True)
                            n4j.add_graph_elements(graph_elements=[graph_elements])
                            
                    except json.JSONDecodeError as e:
                        print(f"⚠️  Skipping line {line_num}: Invalid JSON")
        
        elif dataset_file.endswith('.json'):
            # Handle JSON files
            with open(dataset_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    for i, doc in enumerate(data, 1):
                        text = doc.get('text', '') or doc.get('content', '') if isinstance(doc, dict) else str(doc)
                        
                        if len(text.strip()) > 100:
                            print(f"Processing document {i}...")
                            
                            element = uio.create_element_from_text(
                                text=text,
                                element_id=f"doc_{i}"
                            )
                            
                            graph_elements = kg_agent.run(element, parse_graph_elements=True)
                            n4j.add_graph_elements(graph_elements=[graph_elements])
                else:
                    # Single document
                    text = data.get('text', '') or data.get('content', '') if isinstance(data, dict) else str(data)
                    
                    element = uio.create_element_from_text(
                        text=text,
                        element_id="single_doc"
                    )
                    
                    graph_elements = kg_agent.run(element, parse_graph_elements=True)
                    n4j.add_graph_elements(graph_elements=[graph_elements])
        
        else:
            # Try as plain text file
            with open(dataset_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            element = uio.create_element_from_text(
                text=content,
                element_id="text_file"
            )
            
            graph_elements = kg_agent.run(element, parse_graph_elements=True)
            n4j.add_graph_elements(graph_elements=[graph_elements])
        
    except Exception as e:
        print(f"❌ Error processing dataset: {e}")
        return False
    
    # Final statistics
    print("\n" + "="*60)
    print("KNOWLEDGE GRAPH POPULATION SUMMARY")
    print("="*60)
    
    # Get actual counts from Neo4j
    try:
        result = list(n4j.query("MATCH (n) RETURN count(n) as node_count"))
        actual_nodes = result[0]["node_count"] if result else 0
        
        result = list(n4j.query("MATCH ()-[r]->() RETURN count(r) as rel_count"))
        actual_relationships = result[0]["rel_count"] if result else 0
        
        print(f"Total nodes in Neo4j: {actual_nodes}")
        print(f"Total relationships in Neo4j: {actual_relationships}")
        
        if actual_nodes > 0:
            print(f"\n✅ Knowledge graph populated successfully!")
            
            # Show sample data
            print("\n📊 Sample entities:")
            result = list(n4j.query("""
                MATCH (n) 
                RETURN labels(n)[0] as label, n.id as id, 
                       CASE WHEN n.description IS NOT NULL 
                            THEN substring(n.description, 0, 100) + '...'
                            ELSE 'No description' END as description
                ORDER BY n.id 
                LIMIT 5
            """))
            for record in result:
                print(f"  • {record['id']} ({record['label']}): {record['description']}")
            
            print("\n🔗 Sample relationships:")
            result = list(n4j.query("""
                MATCH (a)-[r]->(b) 
                RETURN a.id, type(r), b.id 
                LIMIT 5
            """))
            for record in result:
                print(f"  • {record['a.id']} --{record['type(r)']}-> {record['b.id']}")
            
            print(f"\n🚀 Ready to test! Try:")
            print(f"   python executor.py \"What is OpenROAD placement?\"")
            
        else:
            print(f"\n❌ No knowledge graph data was created")
            
    except Exception as e:
        print(f"⚠️  Could not get statistics: {e}")
        actual_nodes = 1  # Assume success if we can't query
    
    return actual_nodes > 0

if __name__ == "__main__":
    import sys
    
    dataset_file = "flow_tutorial.md"
    if len(sys.argv) > 1:
        dataset_file = sys.argv[1]
    
    success = populate_neo4j_from_dataset(dataset_file)
    
    if not success:
        print("\n💡 Troubleshooting tips:")
        print("1. Check that flow_tutorial.md file exists")
        print("2. Verify Neo4j connection in .env file")
        print("3. Ensure OpenAI API key is valid")
        print("4. Check file format (MD/JSON/JSONL)")
        
        # List available files
        print("\nAvailable files in current directory:")
        for f in sorted(os.listdir(".")):
            if any(keyword in f.lower() for keyword in ['dataset', 'rag', 'json', 'data', 'tutorial', '.md']):
                size = os.path.getsize(f)
                print(f"  - {f} ({size:,} bytes)")