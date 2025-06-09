#!/usr/bin/env python3
"""
Executor for VLSI RAG queries with OpenROAD execution and feedback loop
Supports both Python and Tcl scripts
"""
import sys
import re
import subprocess
import tempfile
import os
from typing import Dict, Any, Optional, Tuple
from pipeline import VLSIRAGPipeline

def extract_code_from_response(text: str) -> Tuple[Optional[str], str]:
    """
    Extract code from markdown code blocks and determine the type.
    Returns: (code, language) where language is 'python', 'tcl', or 'unknown'
    """
    # Look for ```python code blocks
    python_pattern = r"```python\n(.*?)\n```"
    python_matches = re.findall(python_pattern, text, re.DOTALL)
    
    if python_matches:
        return python_matches[0].strip(), 'python'
    
    # Look for ```tcl code blocks
    tcl_pattern = r"```tcl\n(.*?)\n```"
    tcl_matches = re.findall(tcl_pattern, text, re.DOTALL)
    
    if tcl_matches:
        return tcl_matches[0].strip(), 'tcl'
    
    # Look for ``` code blocks without language specification
    general_pattern = r"```\n(.*?)\n```"
    general_matches = re.findall(general_pattern, text, re.DOTALL)
    
    if general_matches:
        code = general_matches[0].strip()
        
        # Heuristics to determine if it's Python or Tcl
        python_indicators = ['import ', 'def ', 'print(', 'openroad', 'ord.', 'if __name__']
        tcl_indicators = ['set ', 'puts ', 'proc ', 'source ', 'read_', 'write_', 'report_']
        
        python_score = sum(1 for indicator in python_indicators if indicator in code)
        tcl_score = sum(1 for indicator in tcl_indicators if indicator in code)
        
        if python_score > tcl_score:
            return code, 'python'
        elif tcl_score > 0:
            return code, 'tcl'
        else:
            # Default to tcl since OpenROAD runs tcl by default
            return code, 'tcl'
    
    return None, 'unknown'

def execute_python_with_openroad(code: str) -> Dict[str, Any]:
    """Execute Python code with OpenROAD using -python flag."""
    if not code:
        return {"error": "No code to execute", "success": False}
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_path = f.name
    
    try:
        print("🐍 Executing Python code with OpenROAD...")
        print(f"Code to execute:\n{'-'*40}")
        print(code)
        print('-'*40)
        
        # FIX: Add -exit flag and use different approach for Python
        process = subprocess.run(
            ['openroad', '-python', '-exit', temp_path],
            capture_output=True,
            text=True,
            timeout=60,  # Increased timeout
            input='\n'   # Send newline to help with interactive mode
        )
        
        result = {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exit_code": process.returncode,
            "success": process.returncode == 0,
            "language": "python"
        }
        
        return result
        
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out after 60 seconds", "success": False, "language": "python"}
    except FileNotFoundError:
        return {"error": "OpenROAD not found. Please install OpenROAD.", "success": False, "language": "python"}
    except Exception as e:
        return {"error": str(e), "success": False, "language": "python"}
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def execute_tcl_with_openroad(code: str) -> Dict[str, Any]:
    """Execute Tcl code with OpenROAD (default mode)."""
    # Check for placeholder paths
    if any(p in code for p in ["path/to/your", "your_design", "example"]):
        return {
            "error": "Invalid placeholder paths detected in script",
            "success": False,
            "language": "tcl"
        }
    if not code:
        return {"error": "No code to execute", "success": False}
    
    # Add error handling and force exit
    tcl_code = f"""
    set_cmd_errors 1
    set_error_propagate 0
    {code}
    
    # Force exit even if errors occur
    puts "EXECUTION_COMPLETE_MARKER"
    flush stdout
    flush stderr
    exit
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tcl', delete=False) as f:
        f.write(tcl_code)
        temp_path = f.name
    
    try:
        process = subprocess.run(
            ['openroad', '-no_init', temp_path],
            capture_output=True,
            text=True,
            timeout=60,
            check=True  # Raise exception on non-zero exit
        )
        
        result = {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exit_code": process.returncode,
            "success": process.returncode == 0,
            "language": "tcl"
        }
        
        return result
        
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out after 60 seconds", "success": False, "language": "tcl"}
    except FileNotFoundError:
        return {"error": "OpenROAD not found. Please install OpenROAD.", "success": False, "language": "tcl"}
    except Exception as e:
        return {"error": str(e), "success": False, "language": "tcl"}
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def execute_openroad_code(code: str, language: str) -> Dict[str, Any]:
    """Execute code with OpenROAD based on language type."""
    print(f"🎯 Detected language: {language}")
    
    if language == 'python':
        print("🐍 Executing as Python script...")
        return execute_python_with_openroad(code)
    elif language == 'tcl':
        print("🔧 Executing as Tcl script...")
        return execute_tcl_with_openroad(code)
    else:
        # Default to Tcl since OpenROAD runs Tcl by default
        print("❓ Unknown language, defaulting to Tcl...")
        return execute_tcl_with_openroad(code)

def improve_code_with_feedback(pipeline: VLSIRAGPipeline, original_query: str, 
                              code: str, language: str, execution_result: Dict[str, Any]) -> str:
    """Get improved code based on execution feedback."""
    language_info = f"The code was identified as {language.upper()}"
    
    feedback_query = f"""
    The original query was: {original_query}
    
    {language_info} and the generated code was:
    ```{language}
    {code}
    ```
    
    But execution failed with:
    - Exit code: {execution_result.get('exit_code', 'Unknown')}
    - STDOUT: {execution_result.get('stdout', 'No output')}
    - STDERR: {execution_result.get('stderr', 'No errors')}
    - Error: {execution_result.get('error', 'No error message')}
    
    Please provide a corrected version of the code that fixes these issues.
    Focus on proper OpenROAD API usage and error handling.
    Make sure to use the correct language ({language.upper()}) and proper syntax.
    """
    
    return pipeline.query(feedback_query)

def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python executor.py '<your query>'")
        print("Example: python executor.py 'generate code to get input pins of instance output53'")
        print("Supports both Python and Tcl OpenROAD scripts")
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
        code, language = extract_code_from_response(response)
        
        if code:
            print("\n" + "="*60)
            print(f"CODE EXECUTION ({language.upper()}):")
            print("="*60)
            
            execution_result = execute_openroad_code(code, language)
            
            if execution_result["success"]:
                print("✅ Code executed successfully!")
                if execution_result.get("stdout"):
                    print(f"📤 Output:\n{execution_result['stdout']}")
            else:
                print(f"❌ {language.upper()} code execution failed!")
                if execution_result.get("stderr"):
                    print(f"⚠️  Error:\n{execution_result['stderr']}")
                if execution_result.get("error"):
                    print(f"💥 Exception: {execution_result['error']}")
                
                # Step 3: Try to improve the code
                print("\n" + "="*60)
                print("ATTEMPTING CODE IMPROVEMENT:")
                print("="*60)
                
                improved_response = improve_code_with_feedback(pipeline, query, code, language, execution_result)
                print(improved_response)
                
                # Try executing improved code
                improved_code, improved_language = extract_code_from_response(improved_response)
                if improved_code:
                    print(f"\n🔧 Executing improved {improved_language.upper()} code...")
                    improved_result = execute_openroad_code(improved_code, improved_language)
                    
                    if improved_result["success"]:
                        print("✅ Improved code executed successfully!")
                        if improved_result.get("stdout"):
                            print(f"📤 Output:\n{improved_result['stdout']}")
                    else:
                        print(f"❌ Improved {improved_language.upper()} code still failed")
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