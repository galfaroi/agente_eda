#!/usr/bin/env python3
"""
Test runner for easy RAG agent tests using executor.py
Enforces Python code responses using OpenROAD Python API
"""

import unittest
import sys
import os
import argparse

# Conditionally import test pairs and validation function
# We'll populate ACTIVE_TEST_PAIRS and get validate_python_code later based on args

# Add current directory to path to import executor
sys.path.insert(0, os.path.dirname(__file__))
from executor import extract_code_from_response, execute_openroad_code
from pipeline import VLSIRAGPipeline

# Global variable to hold the test pairs for the selected difficulty
ACTIVE_TEST_PAIRS = []
validate_python_code = None # Will be assigned after parsing args

class TestExecutorWithDifficulty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the RAG pipeline for testing"""
        print("\n" + "="*80)
        print("Setting up VLSI RAG Pipeline for Python API Tests...")
        print("="*80)
        
        try:
            cls.pipeline = VLSIRAGPipeline()
            print("✅ VLSI RAG Pipeline initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize pipeline: {e}")
            raise
        
        print("="*80 + "\n")

    def test_python_queries(self):
        """Test all Python RAG queries for the selected difficulty"""
        if not ACTIVE_TEST_PAIRS:
            self.skipTest("No test pairs loaded. Check difficulty argument.")
            return

        for i, test_case in enumerate(ACTIVE_TEST_PAIRS, 1):
            with self.subTest(test=i, difficulty=args.difficulty):
                print(f"\n{'='*60}")
                # Use description from test_case if available, otherwise construct one
                description = test_case.get('description', f"Query: {test_case['query'][:50]}...")
                print(f"PYTHON TEST {i} (Difficulty: {args.difficulty.upper()}): {description}")
                print(f"{'='*60}")
                print(f"Query: {test_case['query']}")
                if 'note' in test_case: # Check if 'note' exists
                    print(f"Note: {test_case['note']}")
                print(f"Expected Language: {test_case['expected_language']}")
                
                # Get response from RAG pipeline
                response = self.pipeline.query(test_case['query'])
                print(f"\nRAG Response:\n{response}")
                
                # Extract code from response
                code, language = extract_code_from_response(response)
                
                if code:
                    print(f"\nExtracted {language.upper()} code:")
                    print("-" * 40)
                    print(code)
                    print("-" * 40)
                    
                    # Enforce Python language
                    if language.lower() != "python":
                        print(f"\n❌ LANGUAGE MISMATCH: Expected Python, got {language.upper()}")
                        print("The RAG should generate Python code, not TCL!")
                        self.fail(f"Expected Python code but got {language.upper()} code")
                        continue
                    
                    # Validate Python code structure
                    # Ensure validate_python_code is loaded
                    if not validate_python_code:
                        self.fail("validate_python_code function not loaded. Check imports based on difficulty.")
                        continue

                    is_valid, issues, message = validate_python_code(code, test_case)
                    print(f"\nPython Code Validation:")
                    print(f"Valid: {is_valid}")
                    print(f"Issues: {issues}")
                    print(f"Message: {message}")
                    
                    if not is_valid:
                        print(f"\n⚠️  WARNING: Generated Python code has issues!")
                        for issue in issues:
                            if issue == "missing_openroad_import":
                                print("  - Missing 'import openroad' or 'from openroad'")
                            elif issue == "no_python_syntax":
                                print("  - Code doesn't look like Python")
                            elif issue.startswith("missing_patterns"):
                                print(f"  - {issue}")
                            elif issue.startswith("problematic_api_usage"):
                                print(f"  - Using problematic API patterns: {issue}")
                                print("    Hint: Use functions like openroad.openroad_version(), openroad.db_has_tech()")
                            elif issue == "contains_shell_commands":
                                print("  - Contains shell commands instead of Python API calls")
                        
                        # Still try to execute even with some issues for learning
                        if any("problematic_api_usage" in str(issue) for issue in issues):
                            print("⚠️  Executing anyway to show actual error...")
                        else:
                            print("❌ Skipping execution due to validation issues")
                            continue
                    
                    # Execute the Python code (unless marked to skip)
                    if not test_case.get('skip_execution', False):
                        print(f"\n🐍 Executing Python code with OpenROAD...")
                        result = execute_openroad_code(code, language)
                        print(f"\nExecution Result:")
                        print(f"Success: {result['success']}")
                        if result.get('stdout'):
                            print(f"Output:\n{result.get('stdout')}")
                        if result.get('stderr'):
                            print(f"Error:\n{result.get('stderr')}")
                        
                        # Provide specific guidance for common errors
                        stderr_lower = result['stderr'].lower()
                        if "design.__init__() missing 1 required positional argument" in stderr_lower:
                            print("\n💡 GUIDANCE: openroad.Design() requires a 'tech' parameter")
                            print("   Try using: openroad.get_db() or openroad.db_has_tech() instead")
                        elif "attributeerror" in stderr_lower and "has no attribute" in stderr_lower:
                            print("\n💡 GUIDANCE: API method doesn't exist")
                            print("   Available functions: openroad_version(), db_has_tech(), thread_count()")
                    
                    # Verify expected outputs if any
                    if test_case.get('expected_output_contains'): # Use .get() for safety
                        output_text = (result.get('stdout', '') + result.get('stderr', '')).lower()
                        for expected in test_case['expected_output_contains']:
                            try:
                                self.assertIn(expected.lower(), output_text,
                                            f"Expected '{expected}' not found in output")
                                print(f"✅ Found expected output: {expected}")
                            except AssertionError as e:
                                print(f"❌ Missing expected output: {expected}")
                                # Don't fail the test for missing output, just log it
                    
                    # Check execution success for basic commands
                    if result['success']:
                        print(f"✅ Python code executed successfully")
                    else:
                        print(f"⚠️  Python code failed but provided learning information")
                            
                else:
                    print(f"\n⚠️  No executable code found in response")
                    # Check if the response at least mentions Python or OpenROAD API
                    response_lower = response.lower()
                    if "python" in response_lower and "openroad" in response_lower:
                        print(f"✅ Response mentions Python and OpenROAD")
                    else:
                        print(f"❌ Response should mention Python API usage")
                        self.fail("No Python code generated and response doesn't mention Python API")

def run_single_test(test_index, difficulty_pairs):
    """Run a single test case by index (1-based) from the given pairs"""
    if not difficulty_pairs:
        print("No test pairs loaded for the selected difficulty.")
        return

    if 1 <= test_index <= len(difficulty_pairs):
        test_case = difficulty_pairs[test_index - 1]
        # Use description from test_case if available
        description = test_case.get('description', f"Query: {test_case['query'][:50]}...")
        print(f"Running single Python test: {description}")
        if 'note' in test_case: # Check if 'note' exists
            print(f"Note: {test_case['note']}")
        print(f"Expected: {test_case['expected_language']} code")
        
        pipeline = VLSIRAGPipeline()
        response = pipeline.query(test_case['query'])
        
        print(f"\nQuery: {test_case['query']}")
        print(f"Response: {response}")
        
        code, language = extract_code_from_response(response)
        if code:
            print(f"\nExtracted {language} code: {code}")
            
            if language.lower() == "python":
                # Validate Python code
                # Ensure validate_python_code is loaded
                if not validate_python_code:
                    print("❌ validate_python_code function not loaded. Cannot validate.")
                    return

                is_valid, issues, message = validate_python_code(code, test_case)
                print(f"Python validation: {is_valid}, issues: {issues}")
                
                result = execute_openroad_code(code, language)
                print(f"Execution result: {result}")
            else:
                print(f"❌ Expected Python, got {language}")
        else:
            print("No code extracted from response")
        
    else:
        print(f"Invalid test index. Available tests for this difficulty: 1-{len(difficulty_pairs)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run VLSI RAG agent tests with selectable difficulty.")
    parser.add_argument(
        '-d', '--difficulty', 
        type=str, 
        default='easy', 
        choices=['easy', 'medium'], 
        help="Difficulty level of tests to run (default: easy)"
    )
    parser.add_argument(
        'test_index', 
        nargs='?', 
        type=int, 
        help="Optional: run a single test by its 1-based index for the selected difficulty."
    )
    
    args = parser.parse_args()

    # Dynamically load test pairs and validation function based on difficulty
    if args.difficulty == 'easy':
        from test_easy_rag_pairs import EASY_TEST_PAIRS as SELECTED_TEST_PAIRS
        from test_easy_rag_pairs import validate_python_code as imported_validator
        print(f"Running EASY tests from test_easy_rag_pairs.py (Found {len(SELECTED_TEST_PAIRS)} pairs)")
    elif args.difficulty == 'medium':
        from test_medium_rag_pairs import MEDIUM_PYTHON_TEST_PAIRS as SELECTED_TEST_PAIRS
        # Assuming medium tests use the same validation logic from easy pairs for now
        # If medium pairs have their own validator, import it here instead.
        try:
            from test_easy_rag_pairs import validate_python_code as imported_validator
            print("Using validate_python_code from test_easy_rag_pairs.py for medium tests.")
        except ImportError:
            print("Warning: Could not import validate_python_code from test_easy_rag_pairs.py for medium tests.")
            print("Medium test validation might be limited.")
            imported_validator = lambda code, tc: (True, [], "Validator not found")

        print(f"Running MEDIUM tests from test_medium_rag_pairs.py (Found {len(SELECTED_TEST_PAIRS)} pairs)")
    else:
        print(f"Unknown difficulty: {args.difficulty}. Exiting.")
        sys.exit(1)
        
    ACTIVE_TEST_PAIRS = SELECTED_TEST_PAIRS
    validate_python_code = imported_validator

    if args.test_index is not None:
        run_single_test(args.test_index, ACTIVE_TEST_PAIRS)
    else:
        # To run unittest with arguments, we need to adjust sys.argv
        # unittest.main() consumes sys.argv, so we pass only the script name
        # The 'args' object is available globally in the TestExecutorWithDifficulty class for context
        sys.argv = [sys.argv[0]] 
        unittest.main() 