#!/usr/bin/env python3
"""
Easy test pairs for Tcl RAG agent based on OpenROAD Tcl API
Updated with EXACT OpenROAD Tcl API command names
"""

TCL_TEST_PAIRS = [
    {
        "query": "Write a Tcl script to load a Liberty (.lib) file 'platforms/lib/NangateOpenCellLibrary_typical.lib'.",
        "expected_language": "tcl",
        "expected_tcl_patterns": ["read_liberty platforms/lib/NangateOpenCellLibrary_typical.lib"],
        "expected_output_contains": [],
        "description": "Load Liberty file",
        "note": "Use the read_liberty command with the file path"
    },
    {
        "query": "Write a Tcl script to load a LEF file 'platforms/lef/NangateOpenCellLibrary.tech.lef'.",
        "expected_language": "tcl",
        "expected_tcl_patterns": ["read_lef platforms/lef/NangateOpenCellLibrary.tech.lef"],
        "expected_output_contains": [],
        "description": "Load LEF file",
        "note": "Use the read_lef command with the file path"
    },
    {
        "query": "Write a Tcl script to load a Verilog netlist 'designs/gcd.v'.",
        "expected_language": "tcl",
        "expected_tcl_patterns": ["read_verilog designs/gcd.v"],
        "expected_output_contains": [],
        "description": "Load Verilog netlist",
        "note": "Use the read_verilog command with the file name"
    },
    {
        "query": "Write a Tcl script to load an ODB database file 'designs/gcd.odb'.",
        "expected_language": "tcl",
        "expected_tcl_patterns": ["read_db designs/gcd.odb"],
        "expected_output_contains": [],
        "description": "Load ODB database",
        "note": "Use the read_db command with the file name"
    },
    {
        "query": "Write a Tcl script to load a DEF placed design file 'designs/gcd.def'.",
        "expected_language": "tcl",
        "expected_tcl_patterns": ["read_def designs/gcd.def"],
        "expected_output_contains": [],
        "description": "Load DEF file",
        "note": "Use the read_def command with the file name"
    }
]

def run_easy_tests():
    """Function to print Tcl test pairs summary."""
    print("Running Easy Tcl RAG Agent Tests")
    print("Updated with EXACT OpenROAD Tcl API command names")
    print("=" * 50)
    for i, test in enumerate(TCL_TEST_PAIRS, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"Query: {test['query']}")
        print(f"Expected Language: {test.get('expected_language', 'tcl')}")
        print(f"Expected Tcl Patterns: {test['expected_tcl_patterns']}")
        print(f"Expected Output Contains: {test.get('expected_output_contains', [])}")
        print(f"Note: {test.get('note', '')}")
        print("-" * 30)
    print()

if __name__ == "__main__":
    run_easy_tests() 