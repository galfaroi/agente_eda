#!/usr/bin/env python3
"""
Ingest session1 tutorial files into both vector database (Qdrant) and Neo4j graph database
These files contain the specific OpenROAD patterns that the hard tests expect.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any

from camel.embeddings import OpenAIEmbedding
from camel.types import EmbeddingModelType
from camel.storages import QdrantStorage, Neo4jGraph
from camel.retrievers import VectorRetriever

def load_session1_files() -> List[Dict[str, Any]]:
    """Load and parse all session1 tutorial files"""
    print("📖 Loading session1 tutorial files...")
    
    session1_dir = Path("session1")
    if not session1_dir.exists():
        print(f"❌ Session1 directory not found: {session1_dir}")
        return []
    
    documents = []
    
    # Python files to process
    python_files = [
        "demo1_flow.py",
        "demo1_helpers.py", 
        "demo1_query.py",
        "demo2_IR.py",
        "demo2_IR_helpers.py",
        "demo2_gate_sizing.py",
        "demo2_gate_sizing_helpers.py"
    ]
    
    for filename in python_files:
        file_path = session1_dir / filename
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Create document entry
                doc = {
                    'id': f"session1_{filename}",
                    'filename': filename,
                    'filepath': str(file_path),
                    'content': content,
                    'source': 'session1_tutorials',
                    'type': 'python_code'
                }
                
                documents.append(doc)
                print(f"   ✅ Loaded {filename} ({len(content)} chars)")
                
            except Exception as e:
                print(f"   ❌ Error loading {filename}: {e}")
    
    # Also load README.md for context
    readme_path = session1_dir / "README.md"
    if readme_path.exists():
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            doc = {
                'id': 'session1_README.md',
                'filename': 'README.md',
                'filepath': str(readme_path),
                'content': content,
                'source': 'session1_tutorials',
                'type': 'documentation'
            }
            
            documents.append(doc)
            print(f"   ✅ Loaded README.md ({len(content)} chars)")
            
        except Exception as e:
            print(f"   ❌ Error loading README.md: {e}")
    
    print(f"✅ Loaded {len(documents)} session1 tutorial files")
    return documents

def extract_openroad_patterns(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract specific OpenROAD patterns from the tutorial files"""
    print("🔍 Extracting OpenROAD patterns from tutorial files...")
    
    patterns = []
    
    # Key patterns to extract
    important_patterns = [
        'initFloorplan', 'getBlock', 'setSpecial', 'globalConnect',
        'getFloorplan', 'addGlobalConnect', 'getTritonCts', 'getReplace',
        'getGlobalRouter', 'getTritonRoute', 'getOpendp', 'makeTracks',
        'detailedPlacement', 'globalRoute', 'runTritonCts'
    ]
    
    for doc in documents:
        if doc['type'] == 'python_code':
            content = doc['content']
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                for pattern in important_patterns:
                    if pattern in line and not line.strip().startswith('#'):
                        # Extract context around the pattern
                        start_idx = max(0, i - 3)
                        end_idx = min(len(lines), i + 4)
                        context_lines = lines[start_idx:end_idx]
                        context = '\n'.join(context_lines)
                        
                        pattern_doc = {
                            'id': f"pattern_{pattern}_{doc['filename']}_{i}",
                            'pattern': pattern,
                            'line_number': i + 1,
                            'source_file': doc['filename'],
                            'context': context,
                            'full_line': line.strip(),
                            'source': 'session1_patterns',
                            'type': 'openroad_pattern'
                        }
                        
                        patterns.append(pattern_doc)
    
    print(f"✅ Extracted {len(patterns)} OpenROAD patterns")
    return patterns

def ingest_session1_to_vector_database(documents: List[Dict[str, Any]], patterns: List[Dict[str, Any]]):
    """Ingest session1 data into Qdrant vector database"""
    print("\n📊 INGESTING SESSION1 DATA INTO VECTOR DATABASE")
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
        
        # Prepare content for ingestion
        all_contents = []
        
        # Add full file contents
        for doc in documents:
            # Split large files into chunks
            content = doc['content']
            if len(content) > 4000:  # Split large files
                chunks = [content[i:i+4000] for i in range(0, len(content), 3000)]  # Overlap
                for j, chunk in enumerate(chunks):
                    chunk_content = f"File: {doc['filename']} (Part {j+1}/{len(chunks)})\n\n{chunk}"
                    all_contents.append(chunk_content)
            else:
                file_content = f"File: {doc['filename']}\n\n{content}"
                all_contents.append(file_content)
        
        # Add pattern contexts
        for pattern in patterns:
            pattern_content = f"OpenROAD Pattern: {pattern['pattern']}\nFile: {pattern['source_file']} (Line {pattern['line_number']})\nCode: {pattern['full_line']}\n\nContext:\n{pattern['context']}"
            all_contents.append(pattern_content)
        
        print(f"🔧 Adding {len(all_contents)} session1 entries to vector database...")
        
        # Prepare records for batch ingestion
        from camel.storages.vectordb_storages.qdrant_storage import QdrantRecord
        
        records = []
        for i, content in enumerate(all_contents):
            # Generate embedding for the content
            content_embedding = embedding.embed(content)
            
            # Create QdrantRecord
            record = QdrantRecord(
                vector=content_embedding,
                payload={
                    'id': f"session1_content_{i}",
                    'content': content,
                    'source': 'session1_tutorials'
                }
            )
            records.append(record)
            
            if (i + 1) % 10 == 0:
                print(f"   Prepared {i + 1}/{len(all_contents)} records...")
        
        # Add all records
        vector_store.add(records)
        
        print(f"✅ Successfully added {len(records)} session1 entries to vector database")
        
    except Exception as e:
        print(f"❌ Error ingesting session1 to vector database: {e}")
        import traceback
        traceback.print_exc()

def ingest_session1_to_neo4j(documents: List[Dict[str, Any]], patterns: List[Dict[str, Any]]):
    """Ingest session1 data into Neo4j graph database"""
    print("\n🔗 INGESTING SESSION1 DATA INTO NEO4J DATABASE")
    print("=" * 60)
    
    try:
        # Initialize Neo4j connection
        n4j = Neo4jGraph(
            url="neo4j+s://a77d863c.databases.neo4j.io",
            username="neo4j",
            password="f1zopPMnKXlhQAYvugcoLUr8t0s9QruIyYsY0YxBBhU"
        )
        
        # Add tutorial file nodes
        print(f"🔧 Adding {len(documents)} tutorial file nodes...")
        for doc in documents:
            try:
                cypher = f"""
                CREATE (f:TutorialFile {{
                    id: '{doc['id']}',
                    filename: '{doc['filename']}',
                    filepath: '{doc['filepath']}',
                    source: '{doc['source']}',
                    type: '{doc['type']}',
                    content_length: {len(doc['content'])}
                }})
                """
                n4j.query(cypher)
            except Exception as e:
                print(f"   ⚠️ Error adding file {doc['filename']}: {e}")
        
        # Add pattern nodes
        print(f"🔧 Adding {len(patterns)} OpenROAD pattern nodes...")
        for pattern in patterns:
            try:
                # Escape single quotes in content
                context = pattern['context'].replace("'", "\\'").replace('"', '\\"')
                full_line = pattern['full_line'].replace("'", "\\'").replace('"', '\\"')
                
                cypher = f"""
                CREATE (p:OpenROADPattern {{
                    id: '{pattern['id']}',
                    pattern: '{pattern['pattern']}',
                    line_number: {pattern['line_number']},
                    source_file: '{pattern['source_file']}',
                    full_line: '{full_line}',
                    source: '{pattern['source']}',
                    type: '{pattern['type']}'
                }})
                """
                n4j.query(cypher)
            except Exception as e:
                print(f"   ⚠️ Error adding pattern {pattern['pattern']}: {e}")
        
        # Create relationships between patterns and files
        print("🔧 Creating relationships between patterns and files...")
        for pattern in patterns:
            try:
                cypher = f"""
                MATCH (p:OpenROADPattern {{id: '{pattern['id']}'}}), 
                      (f:TutorialFile {{filename: '{pattern['source_file']}'}})
                CREATE (p)-[:FOUND_IN]->(f)
                """
                n4j.query(cypher)
            except Exception as e:
                print(f"   ⚠️ Error creating relationship for {pattern['pattern']}: {e}")
        
        # Group patterns by type
        pattern_groups = {}
        for pattern in patterns:
            pattern_name = pattern['pattern']
            if pattern_name not in pattern_groups:
                pattern_groups[pattern_name] = []
            pattern_groups[pattern_name].append(pattern['id'])
        
        # Create pattern type nodes
        print("🔧 Creating pattern type nodes...")
        for pattern_name, pattern_ids in pattern_groups.items():
            try:
                cypher = f"""
                MERGE (pt:PatternType {{
                    name: '{pattern_name}',
                    source: 'session1_tutorials',
                    usage_count: {len(pattern_ids)}
                }})
                """
                n4j.query(cypher)
                
                # Connect patterns to their type
                for pattern_id in pattern_ids:
                    cypher = f"""
                    MATCH (pt:PatternType {{name: '{pattern_name}'}}), 
                          (p:OpenROADPattern {{id: '{pattern_id}'}})
                    CREATE (p)-[:IS_TYPE]->(pt)
                    """
                    n4j.query(cypher)
                    
            except Exception as e:
                print(f"   ⚠️ Error creating pattern type {pattern_name}: {e}")
        
        print(f"✅ Successfully added session1 data to Neo4j")
        print(f"📊 Created {len(documents)} file nodes, {len(patterns)} pattern nodes, {len(pattern_groups)} pattern types")
        
    except Exception as e:
        print(f"❌ Error ingesting session1 to Neo4j: {e}")

def verify_session1_ingestion():
    """Verify that session1 data was successfully ingested"""
    print("\n🔍 VERIFYING SESSION1 INGESTION")
    print("=" * 60)
    
    # Test vector database searches for key patterns
    try:
        embedding = OpenAIEmbedding(model_type=EmbeddingModelType.TEXT_EMBEDDING_3_LARGE)
        vector_store = QdrantStorage(
            vector_dim=embedding.get_output_dim(),
            path="vector_db/",
            collection_name="documents_collection",
        )
        
        vector_retriever = VectorRetriever(
            embedding_model=embedding,
            storage=vector_store,
        )
        
        # Test searches for hard test patterns
        hard_test_patterns = [
            "initFloorplan", "getBlock", "setSpecial", "globalConnect",
            "getTritonCts", "getReplace", "getGlobalRouter", "getTritonRoute"
        ]
        
        print("📋 Testing vector database searches:")
        for pattern in hard_test_patterns:
            try:
                results = vector_retriever.query(query=pattern, top_k=3)
                print(f"   ✅ '{pattern}': Found {len(results)} results")
            except Exception as e:
                print(f"   ❌ '{pattern}': Error - {e}")
        
    except Exception as e:
        print(f"❌ Error verifying vector database: {e}")
    
    # Test Neo4j database
    try:
        n4j = Neo4jGraph(
            url="neo4j+s://a77d863c.databases.neo4j.io",
            username="neo4j",
            password="f1zopPMnKXlhQAYvugcoLUr8t0s9QruIyYsY0YxBBhU"
        )
        
        # Count nodes
        result = n4j.query("MATCH (n:TutorialFile) RETURN count(n) as count")
        file_count = result[0]['count'] if result else 0
        print(f"🔗 Neo4j: {file_count} tutorial file nodes")
        
        result = n4j.query("MATCH (n:OpenROADPattern) RETURN count(n) as count")
        pattern_count = result[0]['count'] if result else 0
        print(f"🔧 Neo4j: {pattern_count} OpenROAD pattern nodes")
        
        result = n4j.query("MATCH (n:PatternType) RETURN count(n) as count")
        type_count = result[0]['count'] if result else 0
        print(f"📊 Neo4j: {type_count} pattern type nodes")
        
        # Test specific pattern searches
        print("📋 Testing Neo4j pattern searches:")
        hard_test_patterns = ["initFloorplan", "getBlock", "setSpecial", "globalConnect"]
        for pattern in hard_test_patterns:
            result = n4j.query(f"MATCH (n:OpenROADPattern) WHERE n.pattern = '{pattern}' RETURN count(n) as count")
            count = result[0]['count'] if result else 0
            if count > 0:
                print(f"   ✅ Found {count} instances of '{pattern}'")
            else:
                print(f"   ❌ No instances found for '{pattern}'")
        
    except Exception as e:
        print(f"❌ Error verifying Neo4j database: {e}")

def main():
    """Main ingestion function for session1 tutorials"""
    load_dotenv()
    
    print("🚀 INGESTING SESSION1 TUTORIAL FILES INTO RAG DATABASES")
    print("=" * 80)
    
    # Load session1 files
    documents = load_session1_files()
    if not documents:
        print("❌ No session1 files loaded")
        return
    
    # Extract OpenROAD patterns
    patterns = extract_openroad_patterns(documents)
    
    # Ingest into both databases
    ingest_session1_to_vector_database(documents, patterns)
    ingest_session1_to_neo4j(documents, patterns)
    
    # Verify ingestion
    verify_session1_ingestion()
    
    print("\n" + "=" * 80)
    print("✅ SESSION1 INGESTION COMPLETE")
    print("=" * 80)
    print(f"📊 Total files processed: {len(documents)}")
    print(f"🔍 Total patterns extracted: {len(patterns)}")
    print("🎯 The RAG system now has access to session1 tutorial patterns!")
    print("💡 This should significantly improve performance on hard tests!")

if __name__ == "__main__":
    main() 