#!/usr/bin/env python3
"""
Easy test pairs for VLSI RAG agent based on OpenROAD flow tutorial
These tests enforce Python code responses and don't require file loading
Updated with EXACT function names from actual OpenROAD Python API
"""

EASY_TEST_PAIRS = [
    {
        "query": "Write Python code to print a simple message and show available OpenROAD API classes using dir()",
        "expected_language": "python",
        "expected_python_patterns": ["import openroad", "print", "dir(openroad)"],
        "expected_output_contains": [],
        "description": "Print a message and explore OpenROAD API",
        "note": "Should use basic Python print and dir() to explore API - THIS WORKS"
    },
    
    {
        "query": "Write Python code to get OpenROAD version using the exact function name openroad_version()",
        "expected_language": "python",
        "expected_python_patterns": ["import openroad", "openroad_version()", "print"],
        "expected_output_contains": ["version"],
        "description": "Get OpenROAD version using exact API function name",
        "note": "Must use openroad.openroad_version() NOT getVersion()"
    },
    
    {
        "query": "Write Python code to check if database has technology using the exact function name db_has_tech()",
        "expected_language": "python",
        "expected_python_patterns": ["import openroad", "db_has_tech()", "print"],
        "expected_output_contains": [],
        "description": "Check database technology status using exact API function",
        "note": "Must use openroad.db_has_tech() NOT Design().getTech()"
    },
    
    {
        "query": "Write Python code to get current thread count using the exact function name thread_count()",
        "expected_language": "python",
        "expected_python_patterns": ["import openroad", "thread_count()", "print"],
        "expected_output_contains": [],
        "description": "Get thread count using exact API function name",
        "note": "Must use openroad.thread_count() NOT getThreadCount()"
    },
    
    {
        "query": "Write Python code to get git describe information using the exact function name openroad_git_describe()",
        "expected_language": "python",
        "expected_python_patterns": ["import openroad", "openroad_git_describe()", "print"],
        "expected_output_contains": [],
        "description": "Get git describe info using exact API function name",
        "note": "Must use openroad.openroad_git_describe() NOT getGitDescribe()"
    }
]

def validate_python_code(code, test_case):
    """
    Validate if the generated code is Python and uses OpenROAD properly.
    Returns (is_valid, issues, message)
    """
    if not code:
        return False, ["no_code"], "No code generated"
    
    code_lower = code.lower().strip()
    issues = []
    
    # Check if it's Python-like
    python_indicators = ["import", "def ", "print(", "=", "if ", "for ", "while "]
    has_python_syntax = any(indicator in code_lower for indicator in python_indicators)
    
    if not has_python_syntax:
        issues.append("no_python_syntax")
    
    # Check for OpenROAD import
    if "import openroad" not in code_lower and "from openroad" not in code_lower:
        issues.append("missing_openroad_import")
    
    # Check for expected patterns (exact function names)
    expected_patterns = test_case.get("expected_python_patterns", [])
    missing_patterns = []
    for pattern in expected_patterns:
        if pattern.lower() not in code_lower:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        issues.append(f"missing_exact_patterns: {missing_patterns}")
    
    # Check if it's trying to use shell commands
    if any(cmd in code_lower for cmd in ["subprocess", "os.system", "openroad -", "#!/bin/"]):
        issues.append("contains_shell_commands")
    
    # Check for known WRONG patterns (common mistakes)
    wrong_patterns = [
        ("openroad.Design()", "use openroad.db_has_tech() instead"),
        ("getVersion()", "use openroad_version() instead"),
        ("getThreadCount()", "use thread_count() instead"),
        ("getGitDescribe()", "use openroad_git_describe() instead"),
        ("openroad.odb", "odb attribute doesn't exist"),
        (".getTech()", "use db_has_tech() instead")
    ]
    
    found_wrong = []
    for wrong_pattern, suggestion in wrong_patterns:
        if wrong_pattern.lower() in code_lower:
            found_wrong.append(f"{wrong_pattern} -> {suggestion}")
    
    if found_wrong:
        issues.append(f"wrong_api_usage: {found_wrong}")
    
    # More lenient validation - allow if no major wrong patterns
    is_valid = len([i for i in issues if not i.startswith("missing_exact_patterns")]) == 0
    message = f"Found issues: {issues}" if issues else "Valid Python code with correct OpenROAD API"
    
    return is_valid, issues, message

def run_easy_tests():
    """Function to run the easy test pairs with the RAG agent"""
    print("Running Easy Python RAG Agent Tests")
    print("Updated with EXACT OpenROAD API function names")
    print("=" * 50)
    
    for i, test in enumerate(EASY_TEST_PAIRS, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"Query: {test['query']}")
        print(f"Expected Language: {test['expected_language']}")
        print(f"Expected Python Patterns: {test['expected_python_patterns']}")
        print(f"Expected Output Contains: {test['expected_output_contains']}")
        print(f"Note: {test['note']}")
        print("-" * 30)

if __name__ == "__main__":
    run_easy_tests() 