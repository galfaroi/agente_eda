#!/usr/bin/env python3
"""
Executor for VLSI RAG queries with OpenROAD execution and feedback loop
"""
import sys
import re
import subprocess
import tempfile
import os
from typing import Dict, Any
from pipeline import VLSIRAGPipeline

def extract_python_code(text: str) -> str:
    """Extract Python code from markdown code blocks."""
    # Look for ```python code blocks
    python_pattern = r"```python\n(.*?)\n```"
    matches = re.findall(python_pattern, text, re.DOTALL)
    
    if matches:
        return matches[0].strip()
    
    # Look for ``` code blocks without language specification
    general_pattern = r"```\n(.*?)\n```"
    matches = re.findall(general_pattern, text, re.DOTALL)
    
    if matches:
        # Check if it looks like Python code
        code = matches[0].strip()
        if any(keyword in code for keyword in ['import', 'def ', 'print(', 'openroad', 'ord.']):
            return code
    
    return None

def execute_openroad_code(code: str) -> Dict[str, Any]:
    """Execute Python code with OpenROAD."""
    if not code:
        return {"error": "No code to execute", "success": False}
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_path = f.name
    
    try:
        print("🔧 Executing with OpenROAD...")
        print(f"Code to execute:\n{'-'*40}")
        print(code)
        print('-'*40)
        
        # Execute with OpenROAD
        process = subprocess.run(
            ['openroad', '-python', temp_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        result = {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exit_code": process.returncode,
            "success": process.returncode == 0
        }
        
        return result
        
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out", "success": False}
    except FileNotFoundError:
        return {"error": "OpenROAD not found. Please install OpenROAD.", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def improve_code_with_feedback(pipeline: VLSIRAGPipeline, original_query: str, 
                              code: str, execution_result: Dict[str, Any]) -> str:
    """Get improved code based on execution feedback."""
    feedback_query = f"""
    The original query was: {original_query}
    
    The generated code was:
    ```python
    {code}
    ```
    
    But execution failed with:
    - Exit code: {execution_result.get('exit_code', 'Unknown')}
    - STDOUT: {execution_result.get('stdout', 'No output')}
    - STDERR: {execution_result.get('stderr', 'No errors')}
    - Error: {execution_result.get('error', 'No error message')}
    
    Please provide a corrected version of the code that fixes these issues.
    Focus on proper OpenROAD API usage and error handling.
    """
    
    return pipeline.query(feedback_query)

def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python executor.py '<your query>'")
        print("Example: python executor.py 'generate code to get input pins of instance output53'")
        return
    
    query = " ".join(sys.argv[1:])
    
    try:
        print("🚀 Initializing VLSI RAG Pipeline...")
        pipeline = VLSIRAGPipeline()
        
        print(f"\n🔍 Processing query: {query}")
        
        # Step 1: Get initial response
        response = pipeline.query(query)
        
        print("\n" + "="*60)
        print("INITIAL RESPONSE:")
        print("="*60)
        print(response)
        
        # Step 2: Extract and execute code
        code = extract_python_code(response)
        
        if code:
            print("\n" + "="*60)
            print("CODE EXECUTION:")
            print("="*60)
            
            execution_result = execute_openroad_code(code)
            
            if execution_result["success"]:
                print("✅ Code executed successfully!")
                if execution_result.get("stdout"):
                    print(f"📤 Output:\n{execution_result['stdout']}")
            else:
                print("❌ Code execution failed!")
                if execution_result.get("stderr"):
                    print(f"⚠️  Error:\n{execution_result['stderr']}")
                if execution_result.get("error"):
                    print(f"💥 Exception: {execution_result['error']}")
                
                # Step 3: Try to improve the code
                print("\n" + "="*60)
                print("ATTEMPTING CODE IMPROVEMENT:")
                print("="*60)
                
                improved_response = improve_code_with_feedback(pipeline, query, code, execution_result)
                print(improved_response)
                
                # Try executing improved code
                improved_code = extract_python_code(improved_response)
                if improved_code:
                    print("\n🔧 Executing improved code...")
                    improved_result = execute_openroad_code(improved_code)
                    
                    if improved_result["success"]:
                        print("✅ Improved code executed successfully!")
                        if improved_result.get("stdout"):
                            print(f"📤 Output:\n{improved_result['stdout']}")
                    else:
                        print("❌ Improved code still failed")
                        if improved_result.get("stderr"):
                            print(f"⚠️  Error:\n{improved_result['stderr']}")
        else:
            print("\n⚠️  No executable code found in response")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 