from pipeline import VLSIRAGPipeline

def debug_retrieval():
    pipeline = VLSIRAGPipeline()
    query = 'Create a Python script that performs floorplanning with a die area of 45x45 microns and core area from (5,5) to (40,40) microns. Use the exact OpenROAD API patterns from tutorial1.'
    
    print('=== VECTOR SEARCH RESULTS ===')
    vector_results = pipeline.vector_retriever.query(query=query, top_k=10, similarity_threshold=0.1)
    
    if not vector_results:
        print("❌ No vector results found!")
    else:
        print(f"✅ Found vector results:")
        print(f"Content length: {len(vector_results)}")
        print(f"Content preview: {vector_results[:500]}...")
    
    print('\n=== CHECKING SPECIFIC TUTORIAL1 PATTERNS ===')
    tutorial1_patterns = [
        'floorplan = design.getFloorplan()',
        'die_area = odb.Rect(',
        'floorplan.initFloorplan(die_area, core_area)',
        'floorplan.makeTracks()',
        'design.micronToDBU('
    ]
    
    for pattern in tutorial1_patterns:
        if pattern in vector_results:
            print(f"✅ Found pattern: {pattern}")
        else:
            print(f"❌ Missing pattern: {pattern}")
    
    print('\n=== TESTING SPECIFIC FLOORPLAN QUERIES ===')
    specific_queries = [
        'floorplan initFloorplan',
        'odb.Rect die_area core_area',
        'design.getFloorplan makeTracks',
        'micronToDBU floorplan tutorial1',
        'demo1_flow.py floorplanning'
    ]
    
    for test_query in specific_queries:
        print(f"\nTesting query: '{test_query}'")
        result = pipeline.vector_retriever.query(query=test_query, top_k=3, similarity_threshold=0.1)
        if result and len(result) > 50:
            print(f"✅ Found {len(result)} chars")
            # Check for tutorial1 patterns
            found_patterns = [p for p in tutorial1_patterns if p in result]
            if found_patterns:
                print(f"✅ Contains tutorial1 patterns: {found_patterns}")
            else:
                print("❌ No tutorial1 patterns found")
        else:
            print("❌ No meaningful results")

if __name__ == "__main__":
    debug_retrieval() 