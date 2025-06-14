#!/usr/bin/env python3
"""
Test executor for HARD tests using NO RAG pipeline (ablation study)
"""
import unittest
import sys
import os
import re
import tempfile
import subprocess
import argparse

# Import the no-RAG pipeline
from pipeline_no_rag import VLSIRAGPipeline

def load_test_pairs(difficulty):
    """Load test pairs based on difficulty level."""
    if difficulty == "easy":
        from test_easy_rag_pairs import EASY_TEST_PAIRS
        return EASY_TEST_PAIRS
    elif difficulty == "medium":
        from test_medium_rag_pairs import MEDIUM_PYTHON_TEST_PAIRS
        return MEDIUM_PYTHON_TEST_PAIRS
    elif difficulty == "hard":
        from test_hard_rag_pairs import HARD_PYTHON_TEST_PAIRS
        return HARD_PYTHON_TEST_PAIRS
    else:
        raise ValueError(f"Unknown difficulty: {difficulty}")

def extract_code_from_response(response: str, expected_language: str) -> str:
    """Extract code from the RAG response."""
    if expected_language.lower() == "python":
        # Look for Python code blocks
        python_pattern = r'```python\n(.*?)\n```'
        matches = re.findall(python_pattern, response, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        # Fallback: look for any code that starts with import
        lines = response.split('\n')
        code_lines = []
        in_code = False
        for line in lines:
            if line.strip().startswith('import') or line.strip().startswith('from'):
                in_code = True
            if in_code:
                code_lines.append(line)
                if line.strip() == '' and len(code_lines) > 3:
                    break
        
        if code_lines:
            return '\n'.join(code_lines).strip()
    
    return response.strip()

def validate_hard_python_code(code: str, expected_patterns: list = None) -> tuple[bool, list, str]:
    """Validate hard Python code structure and complex OpenROAD API usage."""
    issues = []
    
    # Check for basic Python structure
    python_indicators = ["import", "def ", "print(", "=", "if ", "for ", "while ", "tech =", "design ="]
    if not any(indicator in code for indicator in python_indicators):
        issues.append("missing_python_structure")
    
    # Check for OpenROAD import
    if "import openroad" not in code and "from openroad" not in code:
        issues.append("missing_openroad_import")
    
    # Check for expected complex patterns if provided
    if expected_patterns:
        missing_patterns = []
        for pattern in expected_patterns:
            if pattern not in code:
                missing_patterns.append(pattern)
        if missing_patterns:
            issues.append(f"missing_complex_patterns: {missing_patterns}")
    
    # Check for problematic API usage patterns
    problematic_patterns = []
    if "design.addGlobalConnection(" in code:
        problematic_patterns.append("design.addGlobalConnection( -> use design.getBlock().addGlobalConnect() instead")
    
    if problematic_patterns:
        issues.append(f"problematic_api_usage: {problematic_patterns}")
    
    # Check for shell commands instead of Python API
    shell_indicators = ["subprocess", "os.system", "os.popen", "shell=True"]
    if any(indicator in code for indicator in shell_indicators):
        issues.append("contains_shell_commands")
    
    # Check for basic syntax validity
    try:
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        issues.append(f"syntax_error: {str(e)}")
    
    is_valid = len(issues) == 0
    message = "Valid Python code with correct OpenROAD API" if is_valid else f"Found issues: {issues}"
    
    return is_valid, issues, message

def execute_openroad_code(code: str) -> tuple[bool, str]:
    """Execute OpenROAD Python code and return success status and output."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute with OpenROAD
        result = subprocess.run(
            ['openroad', '-python', temp_file],
            capture_output=True,
            text=True,
            timeout=60  # Longer timeout for hard tests
        )
        
        # Clean up
        os.unlink(temp_file)
        
        success = result.returncode == 0
        output = result.stdout + result.stderr
        
        return success, output
        
    except subprocess.TimeoutExpired:
        return False, "Execution timed out"
    except Exception as e:
        return False, f"Execution error: {str(e)}"

class TestHardRAGPairs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the RAG pipeline once for all tests."""
        print("\n" + "="*80)
        print("Setting up VLSI RAG Pipeline for Python API Tests (NO RAG - Ablation Study)...")
        print("="*80)
        cls.pipeline = VLSIRAGPipeline()
        print("✅ VLSI RAG Pipeline initialized successfully")
        print("="*80)
        print()

    def run_test_for_difficulty(self, difficulty, test_number=None):
        """Run tests for a specific difficulty level."""
        test_pairs = load_test_pairs(difficulty)
        
        if test_number is not None:
            # Run specific test
            if 1 <= test_number <= len(test_pairs):
                test_pairs = [test_pairs[test_number - 1]]
                print(f"Running {difficulty.upper()} test {test_number}")
            else:
                print(f"Invalid test number {test_number}. Available: 1-{len(test_pairs)}")
                return
        else:
            print(f"Running {difficulty.upper()} tests from test_{difficulty}_rag_pairs.py (Found {len(test_pairs)} pairs)")
        
        print()
        
        for i, pair in enumerate(test_pairs, 1):
            actual_test_num = test_number if test_number else i
            print("="*60)
            print(f"{difficulty.upper()} PYTHON TEST {actual_test_num}: {pair.get('description', 'No description')}")
            print("="*60)
            print(f"Query: {pair['query']}")
            if 'note' in pair:
                print(f"Note: {pair['note']}")
            print(f"Expected Language: {pair['expected_language']}")
            print()
            
            # Get RAG response
            response = self.pipeline.query(pair['query'])
            print(f"RAG Response:\n{response}")
            print()
            
            # Extract code
            extracted_code = extract_code_from_response(response, pair['expected_language'])
            print(f"Extracted PYTHON code:")
            print("-" * 40)
            print(extracted_code)
            print("-" * 40)
            print()
            
            # Validate Python code
            expected_patterns = pair.get('expected_python_patterns', [])
            is_valid, issues, message = validate_hard_python_code(extracted_code, expected_patterns)
            print(f"Hard Python Code Validation:")
            print(f"Valid: {is_valid}")
            print(f"Issues: {issues}")
            print(f"Message: {message}")
            print()
            
            # Execute if valid and not marked to skip
            if not pair.get('skip_execution', False):
                if is_valid or len([issue for issue in issues if not issue.startswith('missing_complex_patterns')]) == 0:
                    print("🐍 Executing Hard Python code with OpenROAD...")
                    print(f"🎯 Detected language: {pair['expected_language']}")
                    print("🐍 Executing as Python script...")
                    
                    print("🐍 Executing Python code with OpenROAD...")
                    print("Code to execute:")
                    print("-" * 40)
                    print(extracted_code)
                    print("-" * 40)
                    print()
                    
                    success, output = execute_openroad_code(extracted_code)
                    print(f"Execution Result:")
                    print(f"Success: {success}")
                    print(f"Output:\n{output}")
                    
                    if success:
                        print("✅ Hard Python code executed successfully")
                    else:
                        print("⚠️ Hard Python code failed but provided learning information")
                else:
                    print("❌ Skipping execution due to critical validation issues")
            else:
                print("⏭️  Skipping execution (marked as skip_execution)")
                print("   This test focuses on code structure validation")
                if is_valid:
                    print("✅ Hard Python code structure validated successfully")
                else:
                    # Check if only missing complex patterns
                    critical_issues = [issue for issue in issues if not issue.startswith('missing_complex_patterns')]
                    if len(critical_issues) == 0:
                        print("✅ Hard Python code structure validated successfully")
                    else:
                        print(f"⚠️ WARNING: Generated Python code has issues!")
                        for issue in critical_issues:
                            if issue.startswith('problematic_api_usage'):
                                print(f"  - Problematic API usage detected")
                            elif issue == 'contains_shell_commands':
                                print(f"  - Contains shell commands instead of Python API calls")
                            else:
                                print(f"  - {issue}")
                        print("❌ Skipping execution due to critical validation issues")
            
            print()

    def test_hard_pairs(self):
        """Test hard RAG pairs - this will be called by unittest."""
        # Get command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--difficulty', default='hard', choices=['easy', 'medium', 'hard'])
        parser.add_argument('test_number', nargs='?', type=int, help='Specific test number to run')
        
        # Parse known args to avoid conflicts with unittest
        args, unknown = parser.parse_known_args()
        
        self.run_test_for_difficulty(args.difficulty, args.test_number)

if __name__ == '__main__':
    # Handle command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--difficulty', default='hard', choices=['easy', 'medium', 'hard'])
    parser.add_argument('test_number', nargs='?', type=int, help='Specific test number to run')
    
    args, remaining = parser.parse_known_args()
    
    # Set up test suite
    suite = unittest.TestSuite()
    test_case = TestHardRAGPairs()
    test_case.difficulty = args.difficulty
    test_case.test_number = args.test_number
    
    # Add the test method
    suite.addTest(TestHardRAGPairs('test_hard_pairs'))
    
    # Run the test
    runner = unittest.TextTestRunner(verbosity=0)
    runner.run(suite) 