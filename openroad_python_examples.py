#!/usr/bin/env python3
"""
Working OpenROAD Python API Examples
These examples demonstrate correct usage patterns for the OpenROAD Python API
Based on actual successful executions and API introspection
"""

# Example 1: Basic API Exploration (WORKING)
def explore_openroad_api():
    """Print available OpenROAD API classes and functions"""
    import openroad
    print("Hello, OpenROAD!")
    print("Available OpenROAD API classes:")
    print(', '.join(dir(openroad)))

# Example 2: Get Version Information (CORRECT SYNTAX)
def get_version_info():
    """Get OpenROAD version using correct function name"""
    import openroad
    # Correct: use openroad_version() not getVersion()
    version = openroad.openroad_version()
    print(f"OpenROAD Version: {version}")

# Example 3: Check Database Technology Status (CORRECT SYNTAX)
def check_database_tech():
    """Check if database has technology loaded using correct function"""
    import openroad
    # Correct: use db_has_tech() not openroad.Design()
    has_tech = openroad.db_has_tech()
    print(f"Database has technology: {has_tech}")

# Example 4: Get Thread Count (CORRECT SYNTAX)
def get_thread_count():
    """Get current thread count using correct function name"""
    import openroad
    # Correct: use thread_count() not getThreadCount()
    count = openroad.thread_count()
    print(f"Current thread count: {count}")

# Example 5: Get Git Information (CORRECT SYNTAX)
def get_git_info():
    """Get git describe information using correct function name"""
    import openroad
    # Correct: use openroad_git_describe() not getGitDescribe()
    git_info = openroad.openroad_git_describe()
    print(f"Git describe: {git_info}")

# Example 6: Database Operations (CORRECT SYNTAX)
def database_operations():
    """Demonstrate correct database API usage"""
    import openroad
    # Correct: use functional API, not object instantiation
    db = openroad.get_db()
    db_tech = openroad.get_db_tech()
    db_block = openroad.get_db_block()
    print(f"Database: {db}")
    print(f"Database tech: {db_tech}")
    print(f"Database block: {db_block}")

# Summary of Correct API Patterns:
"""
CORRECT OpenROAD Python API Patterns:

1. FUNCTIONAL STYLE (not object-oriented):
   ✅ openroad.openroad_version()
   ❌ openroad.getVersion()

2. SNAKE_CASE NAMING:
   ✅ openroad.thread_count()
   ❌ openroad.getThreadCount()

3. USE AVAILABLE FUNCTIONS:
   ✅ openroad.db_has_tech()
   ❌ openroad.Design().getTech()

4. COMMON AVAILABLE FUNCTIONS:
   - openroad_version()
   - openroad_git_describe()
   - thread_count()
   - set_thread_count()
   - db_has_tech()
   - get_db()
   - get_db_tech()
   - get_db_block()

5. EXPLORATION PATTERN:
   ✅ dir(openroad) to see available functions
   ✅ Basic Python operations work fine
"""

if __name__ == "__main__":
    print("OpenROAD Python API Correct Usage Examples")
    print("=" * 50)
    explore_openroad_api() 