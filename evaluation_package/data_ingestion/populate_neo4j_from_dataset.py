#!/usr/bin/env python3
"""
Populate Neo4j with VLSI knowledge graph data from ORAssistan_RAG_Dataset
"""
import os
import json
import csv
import argparse # Added for better CLI argument handling
from typing import Dict, List
from dotenv import load_dotenv
from camel.storages import Neo4jGraph
from camel.agents import KnowledgeGraphAgent
from camel.loaders import UnstructuredIO
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig

load_dotenv()

# Helper function to process a single dataset file
def _process_single_file(file_path_to_process: str, n4j: Neo4jGraph, kg_agent: KnowledgeGraphAgent, uio: UnstructuredIO) -> int:
    """Processes a single dataset file and returns the number of processed documents."""
    print(f"📖 Reading dataset from '{file_path_to_process}'...")
    total_processed_in_file = 0

    if not os.path.exists(file_path_to_process):
        print(f"❌ File not found: {file_path_to_process}")
        return 0

    try:
        if file_path_to_process.endswith('.jsonl'):
            with open(file_path_to_process, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        doc = json.loads(line.strip())
                        raw_human_text = doc.get('human') or doc.get('prompt')
                        raw_gpt_text = doc.get('gpt') or doc.get('correct_code')
                        human_text_stripped = str(raw_human_text).strip() if raw_human_text is not None else ""
                        gpt_text_stripped = str(raw_gpt_text).strip() if raw_gpt_text is not None else ""
                        combined_text = f"User Query:\n{human_text_stripped}\n\nAssistant Response:\n{gpt_text_stripped}"
                        text_to_process = combined_text.strip()

                        if line_num <= 2 and (file_path_to_process.endswith("query_dataset.jsonl") or "example" in file_path_to_process.lower()): # Reduced debug output
                            print(f"  [Debug JSONL] Line {line_num} from {os.path.basename(file_path_to_process)} (len {len(text_to_process)}): '{text_to_process[:100].replace('\n', ' ')}...'")

                        if len(text_to_process) > 50:
                            element = uio.create_element_from_text(text=text_to_process, element_id=f"jsonl_{os.path.basename(file_path_to_process)}_{line_num}")
                            graph_elements = kg_agent.run(element, parse_graph_elements=True)
                            n4j.add_graph_elements(graph_elements=[graph_elements])
                            total_processed_in_file += 1
                            if total_processed_in_file % 20 == 0:
                                print(f"  Processed {total_processed_in_file} entries from {os.path.basename(file_path_to_process)}...")
                    except json.JSONDecodeError:
                        print(f"⚠️  Skipping line {line_num} in {file_path_to_process}: Invalid JSON")
                    except Exception as e:
                        print(f"⚠️  Error processing line {line_num} in {file_path_to_process}: {e}")
            print(f"✅ Successfully processed {total_processed_in_file} documents from JSONL file '{file_path_to_process}'")

        elif file_path_to_process.endswith('.csv'):
            with open(file_path_to_process, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                try:
                    header = next(reader)
                    print(f"  Skipped header in {os.path.basename(file_path_to_process)}: {header}")
                except StopIteration:
                    f.seek(0)
                    reader = csv.reader(f)

                for row_num, row in enumerate(reader, 1):
                    try:
                        if len(row) < 2:
                            continue
                        human_text_raw, gpt_text_raw = row[0], row[1]
                        human_text_stripped = str(human_text_raw).strip() if human_text_raw is not None else ""
                        gpt_text_stripped = str(gpt_text_raw).strip() if gpt_text_raw is not None else ""
                        combined_text = f"User Query:\n{human_text_stripped}\n\nAssistant Response:\n{gpt_text_stripped}"
                        text_to_process = combined_text.strip()
                        
                        if row_num <= 2 and ("example" in file_path_to_process.lower()): # Reduced debug output
                            print(f"  [Debug CSV] Row {row_num} from {os.path.basename(file_path_to_process)} (len {len(text_to_process)}): '{text_to_process[:100].replace('\n', ' ')}...'")

                        if len(text_to_process) > 50:
                            element = uio.create_element_from_text(text=text_to_process, element_id=f"csv_{os.path.basename(file_path_to_process)}_{row_num}")
                            graph_elements = kg_agent.run(element, parse_graph_elements=True)
                            n4j.add_graph_elements(graph_elements=[graph_elements])
                            total_processed_in_file += 1
                            if total_processed_in_file % 20 == 0:
                                print(f"  Processed {total_processed_in_file} entries from {os.path.basename(file_path_to_process)}...")
                    except Exception as e:
                        print(f"⚠️  Error processing CSV row {row_num} in {file_path_to_process}: {e}")
            print(f"✅ Successfully processed {total_processed_in_file} documents from CSV file '{file_path_to_process}'")

        elif file_path_to_process.endswith('.md'):
            with open(file_path_to_process, "r", encoding="utf-8") as f:
                md_text = f.read()
            print(f"📚 Read {len(md_text)} characters from markdown file '{file_path_to_process}'")
            if len(md_text.strip()) > 50:
                element = uio.create_element_from_text(text=md_text, element_id=f"md_{os.path.basename(file_path_to_process)}")
                graph_elements = kg_agent.run(element, parse_graph_elements=True)
                n4j.add_graph_elements(graph_elements=[graph_elements])
                total_processed_in_file = 1 # Markdown processed as one document
                print(f"✅ Successfully processed markdown file '{file_path_to_process}' as one document")
            else:
                print(f"⚠️  Skipping markdown file '{file_path_to_process}', content too short.")

        elif file_path_to_process.endswith('.json'):
            with open(file_path_to_process, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            docs_in_json = []
            if isinstance(data, list): # List of documents
                for i, doc_content in enumerate(data, 1):
                    text = doc_content.get('text', '') or doc_content.get('content', '') if isinstance(doc_content, dict) else str(doc_content)
                    if len(text.strip()) > 50:
                        docs_in_json.append({'text': text.strip(), 'id': f"json_list_{os.path.basename(file_path_to_process)}_{i}"})
            elif isinstance(data, dict): # Single document
                text = data.get('text', '') or data.get('content', '')
                if len(text.strip()) > 50:
                    docs_in_json.append({'text': text.strip(), 'id': f"json_dict_{os.path.basename(file_path_to_process)}"})
            
            for doc_data in docs_in_json:
                element = uio.create_element_from_text(text=doc_data['text'], element_id=doc_data['id'])
                graph_elements = kg_agent.run(element, parse_graph_elements=True)
                n4j.add_graph_elements(graph_elements=[graph_elements])
                total_processed_in_file += 1
                if total_processed_in_file % 20 == 0:
                    print(f"  Processed {total_processed_in_file} entries from {os.path.basename(file_path_to_process)}...")
            print(f"✅ Successfully processed {total_processed_in_file} documents from JSON file '{file_path_to_process}'")

        else: # Treat as plain text by default
            with open(file_path_to_process, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"📚 Read {len(content)} characters from text file '{file_path_to_process}'")
            if len(content.strip()) > 50:
                element = uio.create_element_from_text(text=content, element_id=f"txt_{os.path.basename(file_path_to_process)}")
                graph_elements = kg_agent.run(element, parse_graph_elements=True)
                n4j.add_graph_elements(graph_elements=[graph_elements])
                total_processed_in_file = 1
                print(f"✅ Successfully processed text file '{file_path_to_process}' as one document")
            else:
                print(f"⚠️  Skipping text file '{file_path_to_process}', content too short.")
        
    except Exception as e:
        print(f"❌ Error processing file {file_path_to_process}: {e}")
    
    return total_processed_in_file

def populate_neo4j_from_dataset(dataset_input_path: str = "query_dataset.jsonl", clear_db: bool = True): # Added clear_db flag
    """Populate Neo4j with knowledge graph from ORAssistan dataset(s)"""
    
    print("🚀 Starting Neo4j population...")
    
    try:
        n4j = Neo4jGraph(
            url=os.getenv("NEO4J_URL", "neo4j+s://1cd25c52.databases.neo4j.io"), # Use env var
            username=os.getenv("NEO4J_USERNAME", "neo4j"),
            password=os.getenv("NEO4J_PASSWORD", "7P9fYDVO-vBVQxV6Ppeta2bfrTSwxmcfglZIryDb8vA")
        )
        n4j.query("RETURN 1 as test")
        print("✅ Neo4j connected successfully")
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        return False
    
    print("🤖 Initializing Knowledge Graph Agent...")
    try:
        chat_cfg = ChatGPTConfig(temperature=0.1).as_dict()
        openai_model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O_MINI, # Consider making configurable
            model_config_dict=chat_cfg,
        )
        uio = UnstructuredIO()
        kg_agent = KnowledgeGraphAgent(model=openai_model)
        print("✅ KG Agent initialized")
    except Exception as e:
        print(f"❌ KG Agent initialization failed: {e}")
        return False
    
    if clear_db:
        print("🧹 Clearing existing VLSI data from Neo4j...")
        try:
            n4j.query("MATCH (n) DETACH DELETE n")
            print("✅ Cleared existing data")
        except Exception as e:
            print(f"⚠️  Warning: Could not clear data: {e}")
    else:
        print("🔵 Skipping database clearing as per clear_db=False.")

    files_to_process_list = []
    if dataset_input_path.endswith('.filelist'):
        print(f"📄 Processing manifest file: {dataset_input_path}")
        if not os.path.exists(dataset_input_path):
            print(f"❌ Manifest file '{dataset_input_path}' not found.")
            return False
        try:
            with open(dataset_input_path, 'r', encoding='utf-8') as manifest_f:
                for line in manifest_f:
                    file_path = line.strip()
                    if file_path and not file_path.startswith('#'): # Ignore empty lines and comments
                        if os.path.exists(file_path):
                            files_to_process_list.append(file_path)
                        else:
                            print(f"⚠️ Path in manifest not found, skipping: {file_path}")
            if not files_to_process_list:
                print(f"🤷 No valid file paths found in manifest '{dataset_input_path}'.")
                return False
        except Exception as e:
            print(f"❌ Error reading manifest file '{dataset_input_path}': {e}")
            return False
    else:
        if not os.path.exists(dataset_input_path):
            print(f"❌ Dataset file '{dataset_input_path}' not found. If it's a list of files, use .filelist extension.")
            # List available files to help user
            print("Available files (or create a .filelist file with paths):")
            for f_name in os.listdir("."):
                if any(ext in f_name.lower() for ext in ['.md', '.json', '.jsonl', '.csv', '.filelist', 'dataset', 'tutorial']):
                    print(f"  - {f_name}")
            return False
        files_to_process_list.append(dataset_input_path)

    grand_total_processed_docs = 0
    for i, file_to_process in enumerate(files_to_process_list, 1):
        print(f"\n[{i}/{len(files_to_process_list)}] Processing: {file_to_process}")
        processed_count = _process_single_file(file_to_process, n4j, kg_agent, uio)
        grand_total_processed_docs += processed_count
        print(f"Finished processing {file_to_process}. Processed {processed_count} new entries.")

    print(f"\n🏁 All files processed. Total new entries added to Neo4j: {grand_total_processed_docs}")
    
    # Final statistics
    print("\n" + "="*60)
    print("KNOWLEDGE GRAPH POPULATION SUMMARY")
    print("="*60)
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
            print(f"\n❌ No knowledge graph data was created or remains after processing.")
    except Exception as e:
        print(f"⚠️  Could not get statistics: {e}")
        return grand_total_processed_docs > 0 # Return based on processed docs if stats fail

    return grand_total_processed_docs > 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate Neo4j with VLSI knowledge graph data from specified dataset file(s) or a .filelist manifest.")
    parser.add_argument(
        "dataset_input_path", 
        nargs='?', 
        default="query_dataset.jsonl",
        help="Path to the dataset file (JSONL, CSV, MD, JSON, TXT) or a .filelist manifest file listing multiple dataset paths. Defaults to 'query_dataset.jsonl'"
    )
    parser.add_argument(
        "--no-clear",
        action="store_false", # Default is True for clear_db
        dest="clear_db",
        help="Do not clear the existing Neo4j database before populating."
    )
    
    args = parser.parse_args()
    
    success = populate_neo4j_from_dataset(args.dataset_input_path, clear_db=args.clear_db)
    
    if not success:
        print("\n💡 Population may have failed or processed no documents. Troubleshooting tips:")
        print("1. Check dataset file paths and format (JSONL, CSV, MD, JSON, TXT, or .filelist).")
        print("2. If using .filelist, ensure paths inside are correct and files exist.")
        print("3. Verify Neo4j connection details (e.g., in .env file or defaults).")
        print("4. Ensure OpenAI API key is valid.")
        
        print("\nAvailable files in current directory that might be datasets or manifests:")
        for f in sorted(os.listdir(".")):
            if any(keyword in f.lower() for keyword in ['dataset', 'rag', 'json', 'data', 'tutorial', '.md', '.csv', '.jsonl', '.filelist', '.txt']):
                try:
                    size = os.path.getsize(f)
                    print(f"  - {f} ({size:,} bytes)")
                except OSError:
                    print(f"  - {f} (size unavailable)")
    else:
        print("\n🎉 Neo4j population process completed.")