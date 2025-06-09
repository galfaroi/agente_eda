import unittest
import os
import subprocess
import re
from pipeline import VLSIRAGPipeline
from test_config import (
    TEST_OUTPUT_DIR,
    VERIFICATION_POINTS,
    TEST_DESIGNS
)

class TestVLSIRAGByDifficulty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment with OpenROAD"""
        print("\n" + "="*80)
        print("Setting up test environment...")
        print("="*80)
        
        # Verify OpenROAD installation
        try:
            result = subprocess.run(['openroad', '-version'], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError("OpenROAD check failed")
            print(f"✅ OpenROAD version: {result.stdout.strip()}")
        except FileNotFoundError:
            raise RuntimeError("OpenROAD not found. Please install OpenROAD.")

        # Initialize pipeline
        cls.pipeline = VLSIRAGPipeline()
        print("✅ VLSI RAG Pipeline initialized")
        
        # Create test output directory
        os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
        print(f"✅ Created test output directory: {TEST_OUTPUT_DIR}")
        print("="*80 + "\n")

    def execute_openroad_commands(self, commands: str) -> subprocess.CompletedProcess:
        """Execute OpenROAD commands and return result"""
        script_file = os.path.join(TEST_OUTPUT_DIR, 'test_script.tcl')
        
        print("\n" + "-"*40)
        print("📝 Generated TCL script:")
        print("-"*40)
        script_content = commands + "\nexit\n"
        print(script_content)
        print("-"*40)
        
        # Create script with commands
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Run OpenROAD with a shorter timeout
        print("\n🚀 Executing OpenROAD...")
        try:
            result = subprocess.run(
                ['openroad', '-no_init', script_file], 
                capture_output=True, 
                text=True,
                timeout=5  # Shorter timeout
            )
            
            print("\n📊 Execution Results:")
            print("-"*40)
            print(f"Exit code: {result.returncode}")
            if result.stdout:
                print("\nStandard Output:")
                print("-"*20)
                print(result.stdout)
            if result.stderr:
                print("\nStandard Error:")
                print("-"*20)
                print(result.stderr)
            print("-"*40)
            
            return result
            
        except subprocess.TimeoutExpired:
            print("\n⚠️  OpenROAD execution timed out after 5 seconds!")
            return subprocess.CompletedProcess(
                args=['openroad', script_file],
                returncode=-1,
                stdout="",
                stderr="Execution timed out after 5 seconds"
            )

    def test_easy_version(self):
        """Test getting OpenROAD version - Easy"""
        print("\n" + "="*80)
        print("Running Test: Get Version")
        print("="*80)
        
        # Simple version command
        result = self.execute_openroad_commands("version")
        self.assertEqual(result.returncode, 0, f"Command failed:\n{result.stderr}")
        self.assertIn("OpenROAD", result.stdout, "Expected version information")

    def test_easy_help(self):
        """Test getting help - Easy"""
        print("\n" + "="*80)
        print("Running Test: Get Help")
        print("="*80)
        
        # Simple help command
        result = self.execute_openroad_commands("help")
        self.assertEqual(result.returncode, 0, f"Command failed:\n{result.stderr}")
        self.assertTrue(len(result.stdout) > 0, "Expected help output")

    def test_medium_db_info(self):
        """Test database operations - Medium"""
        print("\n" + "="*80)
        print("Running Test: Database Info")
        print("="*80)
        
        commands = """
        # Create a database
        create_database test_db
        # Get database info
        puts "Database created"
        """
        result = self.execute_openroad_commands(commands)
        self.assertEqual(result.returncode, 0, f"Command failed:\n{result.stderr}")
        self.assertIn("Database created", result.stdout, "Expected database creation message")

    def test_hard_command_sequence(self):
        """Test executing a sequence of commands - Hard"""
        print("\n" + "="*80)
        print("Running Test: Command Sequence")
        print("="*80)
        
        commands = """
        # Create database
        create_database test_db
        # Print some info
        puts "Running command sequence"
        # Get help
        help
        """
        result = self.execute_openroad_commands(commands)
        self.assertEqual(result.returncode, 0, f"Command failed:\n{result.stderr}")
        self.assertIn("Running command sequence", result.stdout, "Expected sequence output")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        print("\n" + "="*80)
        print("Cleaning up test environment...")
        print("="*80)
        import shutil
        if os.path.exists(TEST_OUTPUT_DIR):
            shutil.rmtree(TEST_OUTPUT_DIR)
            print(f"✅ Removed test output directory: {TEST_OUTPUT_DIR}")
        print("="*80 + "\n")

if __name__ == '__main__':
    unittest.main() 