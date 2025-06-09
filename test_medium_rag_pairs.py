# test_medium_rag_pairs.py
# Medium difficulty test pairs for VLSI RAG Agent (Python API focused)
# These tests assume OpenROAD is initialized but no specific design/LEF/DEF is loaded.
# They focus on API calls that should be available in a bare OpenROAD Python environment.

MEDIUM_PYTHON_TEST_PAIRS = [
    {
        "query": "Write Python code using the `openroad` module to load a Liberty file at 'platforms/lib/NangateOpenCellLibrary_typical.lib'.",
        "expected_language": "python",
        "expected_python_patterns": [
            "import openroad",
            "tech = openroad.Tech()",
            "tech.readLiberty(\"platforms/lib/NangateOpenCellLibrary_typical.lib\")"
        ],
        "description": "Load Liberty file"
    },
    {
        "query": "Write Python code using the `openroad` module to load a LEF file at 'platforms/lef/NangateOpenCellLibrary.tech.lef'.",
        "expected_language": "python",
        "expected_python_patterns": [
            "import openroad",
            "tech = openroad.Tech()",
            "tech.readLef(\"platforms/lef/NangateOpenCellLibrary.tech.lef\")"
        ],
        "description": "Load LEF file"
    },
    {
        "query": "Write Python code using the `openroad` module to read a Verilog netlist 'designs/gcd.v' and link top module 'gcd'.",
        "expected_language": "python",
        "expected_python_patterns": [
            "import openroad",
            "tech = openroad.Tech()",
            "design = openroad.Design(tech)",
            "design.readVerilog(\"designs/gcd.v\")",
            "design.link(\"gcd\")"
        ],
        "description": "Read Verilog and link top module"
    },
    {
        "query": "Write Python code using the `openroad` module to read an ODB database file 'designs/gcd.odb'.",
        "expected_language": "python",
        "expected_python_patterns": [
            "import openroad",
            "tech = openroad.Tech()",
            "design = openroad.Design(tech)",
            "design.readDb(\"designs/gcd.odb\")"
        ],
        "skip_execution": True,
        "description": "Read ODB database file"
    },
    {
        "query": "Write Python code using the `openroad` module to read a DEF file 'designs/gcd.def'.",
        "expected_language": "python",
        "expected_python_patterns": [
            "import openroad",
            "tech = openroad.Tech()",
            "design = openroad.Design(tech)",
            "design.readDef(\"designs/gcd.def\")"
        ],
        "skip_execution": True,
        "description": "Read DEF placed-design file"
    }
]

if __name__ == '__main__':
    # This is just for basic validation of the data structure
    for i, pair in enumerate(MEDIUM_PYTHON_TEST_PAIRS):
        print(f"Test Pair {i+1}: {pair.get('description', 'N/A')}")
        print(f"  Query: {pair['query']}")
        print(f"  Expected Lang: {pair['expected_language']}")
        print(f"  Expected Patterns: {pair['expected_python_patterns']}")
        print(f"  Notes: {pair['notes']}\\n")

    print(f"Total medium difficulty pairs: {len(MEDIUM_PYTHON_TEST_PAIRS)}") 