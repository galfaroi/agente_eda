#!/usr/bin/env python3
"""
Test runner for TCL RAG agent tests using executor.py
Enforces Tcl code responses using OpenROAD Tcl API
"""

import unittest
import sys
import os
import argparse

# Allow importing executor and pipeline from project root
sys.path.insert(0, os.path.dirname(__file__))
from executor import extract_code_from_response, execute_openroad_code
from pipeline import VLSIRAGPipeline
from test_easy_tcl_pairs import TCL_TEST_PAIRS

class TestExecutorWithTcl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the RAG pipeline with header logging
        print("\n" + "="*80)
        print("Setting up VLSI RAG Pipeline for Tcl API Tests...")
        print("="*80)
        try:
            cls.pipeline = VLSIRAGPipeline()
            print("✅ VLSI RAG Pipeline initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize pipeline: {e}")
            raise
        print("="*80 + "\n")

    def test_tcl_generation(self):
        for i, test_case in enumerate(TCL_TEST_PAIRS, 1):
            with self.subTest(i=i, desc=test_case['description']):
                # Header
                print(f"\n{'='*60}")
                print(f"TCL TEST {i}: {test_case['description']}")
                print(f"{'='*60}")
                print(f"Query: {test_case['query']}")
                if test_case.get('note'):
                    print(f"Note: {test_case['note']}")
                print(f"Expected Language: {test_case.get('expected_language', 'tcl')}")

                # Get and print RAG response
                response = self.pipeline.query(test_case['query'])
                print(f"\nRAG Response:\n{response}")

                # Extract code
                code, language = extract_code_from_response(response)
                # Ensure the response is Tcl
                self.assertEqual(language, 'tcl', f"Expected Tcl code, got {language}")

                if code:
                    # Print extracted code
                    print(f"\nExtracted {language.upper()} code:")
                    print('-'*40)
                    print(code)
                    print('-'*40)
                    # Check expected patterns
                    for pat in test_case['expected_tcl_patterns']:
                        self.assertIn(pat, code, f"Pattern '{pat}' not found in TCL code:\n{code}")
                    # Execute and print result
                    print(f"\n🔧 Executing Tcl script with OpenROAD...")
                    result = execute_openroad_code(code, language)
                    print(f"\nExecution Result:")
                    print(f"Success: {result.get('success')}")
                    if result.get('stdout'):
                        print(f"Output:\n{result.get('stdout')}")
                    if result.get('stderr'):
                        print(f"Error:\n{result.get('stderr')}")
                    # Assert success
                    self.assertTrue(result.get('success', False),
                                    f"Tcl execution failed: stdout={result.get('stdout')}, stderr={result.get('stderr')}")
                else:
                    print("⚠️  No Tcl code found in response")
                    self.fail("No Tcl code generated")

def run_single_test(test_index, test_pairs):
    """Run a single Tcl test case by index (1-based)."""
    if not test_pairs:
        print("No Tcl test pairs loaded.")
        return
    if 1 <= test_index <= len(test_pairs):
        test_case = test_pairs[test_index-1]
        print(f"\nRunning single Tcl test {test_index}: {test_case['description']}")
        # Initialize pipeline
        pipeline = VLSIRAGPipeline()
        print(f"Query: {test_case['query']}")
        response = pipeline.query(test_case['query'])
        print(f"Response:\n{response}")
        code, language = extract_code_from_response(response)
        if language != 'tcl':
            print(f"❌ Expected Tcl code but got {language}")
            return
        for pat in test_case['expected_tcl_patterns']:
            assert pat in code, f"Pattern '{pat}' not found in code: {code}"
        result = execute_openroad_code(code, language)
        if result.get('success', False):
            print("✅ Tcl execution succeeded")
        else:
            print(f"❌ Tcl execution failed: stdout={result.get('stdout')}, stderr={result.get('stderr')}")
    else:
        print(f"Invalid test index {test_index}. Must be 1-{len(test_pairs)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Tcl RAG agent tests.")
    parser.add_argument('test_index', nargs='?', type=int, help="Optional 1-based index to run a single test.")
    args = parser.parse_args()
    if args.test_index is not None:
        run_single_test(args.test_index, TCL_TEST_PAIRS)
    else:
        sys.argv = [sys.argv[0]]
        unittest.main() 