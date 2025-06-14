from pipeline import VLSIRAGPipeline

def check_graph_database():
    pipeline = VLSIRAGPipeline()
    
    print('=== NEO4J GRAPH DATABASE ANALYSIS ===')
    
    # Check total nodes and relationships
    print('\n1. Database Statistics:')
    stats_query = """
    MATCH (n) 
    RETURN labels(n) as label, count(n) as count
    ORDER BY count DESC
    """
    
    results = pipeline.n4j.query(stats_query)
    total_nodes = 0
    for record in results:
        label = record['label'][0] if record['label'] else 'No Label'
        count = record['count']
        total_nodes += count
        print(f"  {label}: {count} nodes")
    
    print(f"  Total nodes: {total_nodes}")
    
    # Check for tutorial1/session1 related content
    print('\n2. Tutorial1/Session1 Content Search:')
    tutorial_searches = [
        ("demo1_flow", "MATCH (n) WHERE n.id CONTAINS 'demo1_flow' OR n.description CONTAINS 'demo1_flow' RETURN n LIMIT 5"),
        ("session1", "MATCH (n) WHERE n.id CONTAINS 'session1' OR n.description CONTAINS 'session1' RETURN n LIMIT 5"),
        ("floorplan", "MATCH (n) WHERE n.id CONTAINS 'floorplan' OR n.description CONTAINS 'floorplan' RETURN n LIMIT 5"),
        ("initFloorplan", "MATCH (n) WHERE n.id CONTAINS 'initFloorplan' OR n.description CONTAINS 'initFloorplan' RETURN n LIMIT 5")
    ]
    
    for search_term, query in tutorial_searches:
        print(f"\n  Searching for '{search_term}':")
        results = pipeline.n4j.query(query)
        if results:
            for i, record in enumerate(results, 1):
                node = record['n']
                print(f"    {i}. ID: {node.get('id', 'N/A')}")
                print(f"       Description: {node.get('description', 'N/A')[:100]}...")
        else:
            print(f"    ❌ No nodes found for '{search_term}'")
    
    # Check for OpenROAD API nodes
    print('\n3. OpenROAD API Nodes:')
    api_query = """
    MATCH (n:OpenROADAPI) 
    RETURN n.function_name as function_name, n.description as description
    ORDER BY n.function_name
    LIMIT 10
    """
    
    results = pipeline.n4j.query(api_query)
    if results:
        print(f"  Found {len(results)} OpenROAD API nodes (showing first 10):")
        for record in results:
            func_name = record['function_name']
            desc = record['description'][:80] if record['description'] else 'No description'
            print(f"    • {func_name}: {desc}...")
    else:
        print("  ❌ No OpenROAD API nodes found")
    
    # Check for tutorial1 specific patterns in API nodes
    print('\n4. Tutorial1 Pattern Search in API Nodes:')
    tutorial1_patterns = [
        'initFloorplan',
        'getFloorplan', 
        'micronToDBU',
        'setSpecial',
        'getReplace',
        'getTritonCts',
        'makeTracks'
    ]
    
    for pattern in tutorial1_patterns:
        pattern_query = f"""
        MATCH (n:OpenROADAPI) 
        WHERE n.function_name CONTAINS '{pattern}' OR n.description CONTAINS '{pattern}'
        RETURN n.function_name as function_name, n.description as description
        LIMIT 3
        """
        
        results = pipeline.n4j.query(pattern_query)
        if results:
            print(f"  ✅ Found '{pattern}':")
            for record in results:
                func_name = record['function_name']
                print(f"    • {func_name}")
        else:
            print(f"  ❌ Missing '{pattern}'")
    
    # Test graph retrieval with tutorial1 query
    print('\n5. Graph Retrieval Test:')
    test_query = "Create a Python script that performs floorplanning with a die area of 45x45 microns and core area from (5,5) to (40,40) microns. Use the exact OpenROAD API patterns from tutorial1."
    
    # Use the same method as in the pipeline
    from camel.loaders import UnstructuredIO
    from camel.agents import KnowledgeGraphAgent
    
    uio = UnstructuredIO()
    kg_agent = KnowledgeGraphAgent(model=pipeline.openai_model)
    
    el = uio.create_element_from_text(text=test_query, element_id="kg_query")
    ans_el = kg_agent.run(el, parse_graph_elements=True)
    
    print(f"  Extracted {len(ans_el.nodes)} nodes from query")
    
    kg_ctx = []
    for node in ans_el.nodes:
        cypher = f"""
        MATCH (n {{id: '{node.id}'}})-[r]->(m)
        RETURN 'Node ' + n.id + ' --' + type(r) + '--> ' + m.id AS desc
        UNION
        MATCH (n)<-[r]-(m {{id: '{node.id}'}})
        RETURN 'Node ' + m.id + ' --' + type(r) + '--> ' + n.id AS desc
        """
        results = pipeline.n4j.query(query=cypher)
        for rec in results:
            kg_ctx.append(rec["desc"])
    
    if kg_ctx:
        print(f"  ✅ Found {len(kg_ctx)} graph relationships:")
        for ctx in kg_ctx[:5]:  # Show first 5
            print(f"    • {ctx}")
    else:
        print("  ❌ No graph relationships found")

if __name__ == "__main__":
    check_graph_database() 