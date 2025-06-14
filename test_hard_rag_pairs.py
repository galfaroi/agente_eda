#!/usr/bin/env python3
"""
Hard difficulty test pairs for VLSI RAG Agent (Python API focused)
These tests require complex OpenROAD operations including floorplanning, placement, routing, and analysis.
They test advanced API usage and multi-step workflows.
"""

HARD_PYTHON_TEST_PAIRS = [
    {
        "query": "Write Python code using the `openroad` module to perform complete floorplanning: load technology files (platforms/lib/NangateOpenCellLibrary_typical.lib and platforms/lef/NangateOpenCellLibrary.tech.lef), create design, read Verilog file designs/gcd.v, link module 'gcd', initialize floorplan with die area (0,0,1000,1000) and core area (100,100,900,900), and create placement rows.",
        "expected_language": "python",
        "expected_python_patterns": [
            "import openroad",
            "tech = openroad.Tech()",
            "tech.readLiberty(",
            "tech.readLef(",
            "design = openroad.Design(tech)",
            "design.readVerilog(",
            "design.link(",
            "floorplan = design.getFloorplan()",
            "floorplan.initFloorplan(",
            "floorplan.makeTracks()"
        ],
        "description": "Complete floorplanning workflow with technology setup",
        "note": "Tests multi-step floorplanning process with proper technology loading using actual files"
    },
    {
        "query": "Write Python code using the `openroad` module to perform power planning: first load technology files (platforms/lib/NangateOpenCellLibrary_typical.lib and platforms/lef/NangateOpenCellLibrary.tech.lef), read DEF file designs/gcd.def, then create VDD and VSS nets, set them as special power/ground nets, configure global connections, and add power stripes on metal layers.",
        "expected_language": "python", 
        "expected_python_patterns": [
            "import openroad",
            "design.getBlock()",
            "odb.dbNet_create(",
            "setSpecial()",
            "setSigType(",
            "addGlobalConnect(",
            "globalConnect()",
            "VDD",
            "VSS"
        ],
        "description": "Power planning with VDD/VSS nets and global connections",
        "note": "Tests power network creation and configuration using actual DEF file",
        "skip_execution": True
    },
    {
        "query": "Write Python code using the `openroad` module to perform global placement: first load technology files (platforms/lib/NangateOpenCellLibrary_typical.lib and platforms/lef/NangateOpenCellLibrary.tech.lef), read Verilog file designs/gcd.v, link module 'gcd', initialize floorplan, then configure the Replace placer with target density 0.7, disable timing-driven mode, set initial placement iterations to 20, and run global placement.",
        "expected_language": "python",
        "expected_python_patterns": [
            "import openroad",
            "gpl = design.getReplace()",
            "gpl.setTargetDensity(0.7)",
            "gpl.setTimingDrivenMode(False)",
            "gpl.setInitialPlaceMaxIter(20)",
            "gpl.doInitialPlace()"
        ],
        "description": "Global placement with Replace placer configuration",
        "note": "Tests placement engine configuration and execution with actual design files",
        "skip_execution": True
    },
    {
        "query": "Write Python code using the `openroad` module to perform clock tree synthesis: first load technology files (platforms/lib/NangateOpenCellLibrary_typical.lib and platforms/lef/NangateOpenCellLibrary.tech.lef), read Verilog file designs/gcd.v, link module 'gcd', initialize floorplan and perform placement, then configure TritonCTS with wire segment unit 20, set buffer lists (CLKBUF_X3, CLKBUF_X1), configure wire RC parameters, and run CTS.",
        "expected_language": "python",
        "expected_python_patterns": [
            "import openroad",
            "cts = design.getTritonCts()",
            "parms = cts.getParms()",
            "parms.setWireSegmentUnit(20)",
            "cts.setBufferList(",
            "cts.setRootBuffer(",
            "cts.setSinkBuffer(",
            "cts.runTritonCts()",
            "design.evalTclString("
        ],
        "description": "Clock tree synthesis with TritonCTS configuration",
        "note": "Tests CTS engine setup and buffer configuration with complete design flow",
        "skip_execution": True
    },
    {
        "query": "Write Python code using the `openroad` module to perform global routing: first load technology files (platforms/lib/NangateOpenCellLibrary_typical.lib and platforms/lef/NangateOpenCellLibrary.tech.lef), read Verilog file designs/gcd.v, link module 'gcd', initialize floorplan, perform placement and CTS, then configure routing layers from metal1 to metal8, set clock layers from metal3 to metal8, configure adjustment factor 0.5, enable verbose mode, and run global routing.",
        "expected_language": "python",
        "expected_python_patterns": [
            "import openroad",
            "grt = design.getGlobalRouter()",
            "design.getTech().getDB().getTech().findLayer(",
            "getRoutingLevel()",
            "grt.setMinRoutingLayer(",
            "grt.setMaxRoutingLayer(",
            "grt.setMinLayerForClock(",
            "grt.setMaxLayerForClock(",
            "grt.setAdjustment(0.5)",
            "grt.setVerbose(True)",
            "grt.globalRoute(True)"
        ],
        "description": "Global routing with layer configuration and parameters",
        "note": "Tests routing engine setup with layer constraints using complete design flow",
        "skip_execution": True
    }
]

def validate_python_code(code, test_case):
    """
    Validate if the generated code is Python and uses OpenROAD properly for hard tests.
    Returns (is_valid, issues, message)
    """
    if not code:
        return False, ["no_code"], "No code generated"
    
    code_lower = code.lower().strip()
    issues = []
    
    # Check if it's Python-like
    python_indicators = ["import", "def ", "print(", "=", "if ", "for ", "while ", "tech =", "design ="]
    has_python_syntax = any(indicator in code_lower for indicator in python_indicators)
    
    if not has_python_syntax:
        issues.append("no_python_syntax")
    
    # Check for OpenROAD import
    if "import openroad" not in code_lower and "from openroad" not in code_lower:
        issues.append("missing_openroad_import")
    
    # Check for expected patterns (complex API usage)
    expected_patterns = test_case.get("expected_python_patterns", [])
    missing_patterns = []
    for pattern in expected_patterns:
        if pattern.lower() not in code_lower:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        issues.append(f"missing_complex_patterns: {missing_patterns}")
    
    # Check if it's trying to use shell commands instead of Python API
    if any(cmd in code_lower for cmd in ["subprocess", "os.system", "openroad -", "#!/bin/", "tcl"]):
        issues.append("contains_shell_commands")
    
    # Check for problematic patterns (common mistakes in hard tests)
    problematic_patterns = [
        ("design.initializeFloorplan(", "use floorplan.initFloorplan() instead"),
        ("design.addGlobalConnection(", "use design.getBlock().addGlobalConnect() instead"),
        ("design.setVoltageDomain(", "use proper power planning APIs"),
        ("design.definePdnGrid(", "use proper power planning APIs"),
        ("design.addPdnRing(", "use proper power planning APIs"),
        ("design.makeSpecialNet(", "use odb.dbNet_create() and setSpecial()"),
        ("openroad.initFloorplan(", "use design.getFloorplan().initFloorplan()"),
        ("openroad.globalPlace(", "use design.getReplace().doInitialPlace()"),
        ("openroad.clockTreeSynthesis(", "use design.getTritonCts().runTritonCts()"),
        ("openroad.globalRoute(", "use design.getGlobalRouter().globalRoute()")
    ]
    
    found_problematic = []
    for problematic_pattern, suggestion in problematic_patterns:
        if problematic_pattern.lower() in code_lower:
            found_problematic.append(f"{problematic_pattern} -> {suggestion}")
    
    if found_problematic:
        issues.append(f"problematic_api_usage: {found_problematic}")
    
    # Check for proper workflow structure (hard tests should have multi-step processes)
    workflow_indicators = [
        "tech =", "design =", "floorplan =", "gpl =", "cts =", "grt =",
        ".readLiberty(", ".readLef(", ".readVerilog(", ".link(",
        ".getFloorplan(", ".getReplace(", ".getTritonCts(", ".getGlobalRouter("
    ]
    
    workflow_count = sum(1 for indicator in workflow_indicators if indicator.lower() in code_lower)
    if workflow_count < 3:  # Hard tests should have multiple workflow steps
        issues.append("insufficient_workflow_complexity")
    
    # More strict validation for hard tests
    critical_issues = [i for i in issues if i in ["no_python_syntax", "missing_openroad_import", "contains_shell_commands", "problematic_api_usage"]]
    is_valid = len(critical_issues) == 0
    
    message = f"Found issues: {issues}" if issues else "Valid complex Python code with correct OpenROAD API workflow"
    
    return is_valid, issues, message

def run_hard_tests():
    """Function to run the hard test pairs with the RAG agent"""
    print("Running Hard Python RAG Agent Tests")
    print("Complex OpenROAD workflows and advanced API usage")
    print("=" * 50)
    
    for i, test in enumerate(HARD_PYTHON_TEST_PAIRS, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"Query: {test['query']}")
        print(f"Expected Language: {test['expected_language']}")
        print(f"Expected Python Patterns: {test['expected_python_patterns']}")
        print(f"Note: {test['note']}")
        print(f"Skip Execution: {test.get('skip_execution', False)}")
        print("-" * 30)

if __name__ == "__main__":
    run_hard_tests() 