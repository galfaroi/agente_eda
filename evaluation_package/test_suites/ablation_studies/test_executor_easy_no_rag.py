#!/usr/bin/env python3
"""
Test executor for EASY tests using NO RAG pipeline (ablation study)
"""
import unittest
import sys
import os
import re
import tempfile
import subprocess

# Import the no-RAG pipeline
from pipeline_no_rag import VLSIRAGPipeline

# Import test pairs
from test_easy_rag_pairs import EASY_TEST_PAIRS as test_pairs

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

def validate_python_code(code: str) -> tuple[bool, list, str]:
    """Validate Python code structure and OpenROAD API usage."""
    issues = []
    
    # Check for basic Python structure
    python_indicators = ["import", "def ", "print(", "=", "if ", "for ", "while ", "tech =", "design ="]
    if not any(indicator in code for indicator in python_indicators):
        issues.append("missing_python_structure")
    
    # Check for OpenROAD import
    if "import openroad" not in code and "from openroad" not in code:
        issues.append("missing_openroad_import")
    
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
            timeout=30
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

class TestEasyRAGPairs(unittest.TestCase):
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

    def test_all_easy_pairs(self):
        """Test all easy RAG pairs."""
        print(f"Running EASY tests from test_easy_rag_pairs.py (Found {len(test_pairs)} pairs)")
        print()
        
        for i, pair in enumerate(test_pairs, 1):
            with self.subTest(test_case=i):
                print("="*60)
                print(f"PYTHON TEST {i} (Difficulty: EASY): {pair.get('description', 'No description')}")
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
                is_valid, issues, message = validate_python_code(extracted_code)
                print(f"Python Code Validation:")
                print(f"Valid: {is_valid}")
                print(f"Issues: {issues}")
                print(f"Message: {message}")
                print()
                
                # Execute if valid
                if is_valid and not pair.get('skip_execution', False):
                    print("🐍 Executing Python code with OpenROAD...")
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
                    
                    # Check for expected patterns in output
                    if 'expected_output_patterns' in pair:
                        for pattern in pair['expected_output_patterns']:
                            if pattern.lower() in output.lower():
                                print(f"✅ Found expected output: {pattern}")
                            else:
                                print(f"⚠️ Missing expected output: {pattern}")
                    
                    if success:
                        print("✅ Python code executed successfully")
                    else:
                        print("❌ Python code execution failed")
                        print(f"Error details: {output}")
                else:
                    if pair.get('skip_execution', False):
                        print("⏭️  Skipping execution (marked as skip_execution)")
                        print("   This test focuses on code structure validation")
                        print("✅ Python code structure validated successfully")
                    else:
                        print("❌ Skipping execution due to validation issues")
                
                print()

if __name__ == '__main__':
    unittest.main() 