#!/usr/bin/env python3
"""
AGENTE VLSI - Package Verification Script
This script verifies that all necessary files are present and paths are correct.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ MISSING {description}: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists and report status."""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ MISSING {description}: {dirpath}")
        return False

def main():
    print("🔍 AGENTE VLSI - Package Verification")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("README_EVALUATION.md"):
        print("❌ Error: Please run this script from the evaluation_package directory")
        sys.exit(1)
    
    all_good = True
    
    print("\n📁 Core System Files:")
    all_good &= check_file_exists("core_system/pipeline.py", "Main RAG Pipeline")
    all_good &= check_file_exists("core_system/pipeline_no_rag.py", "No-RAG Pipeline (Ablation)")
    all_good &= check_file_exists("core_system/executor.py", "Code Executor")
    
    print("\n🧪 Test Suite Files:")
    all_good &= check_file_exists("test_suites/easy/test_easy_rag_pairs.py", "Easy Test Pairs")
    all_good &= check_file_exists("test_suites/easy/test_executor_easy.py", "Easy Test Executor")
    all_good &= check_file_exists("test_suites/medium/test_medium_rag_pairs.py", "Medium Test Pairs")
    all_good &= check_file_exists("test_suites/hard/test_hard_rag_pairs.py", "Hard Test Pairs")
    all_good &= check_file_exists("test_suites/hard/test_executor_hard_new.py", "Hard Test Executor")
    all_good &= check_file_exists("test_suites/ablation_studies/test_executor_easy_no_rag.py", "Easy No-RAG Tests")
    all_good &= check_file_exists("test_suites/ablation_studies/test_executor_hard_no_rag.py", "Hard No-RAG Tests")
    
    print("\n📊 Reports and Documentation:")
    all_good &= check_file_exists("reports/agent_performance_report.md", "Detailed Performance Report")
    all_good &= check_file_exists("reports/performance_summary_table.md", "Performance Summary")
    all_good &= check_file_exists("reports/README.md", "Original README")
    all_good &= check_file_exists("README_EVALUATION.md", "Evaluation Guide")
    
    print("\n🔧 Analysis Tools:")
    all_good &= check_file_exists("analysis_tools/analyze_rag_databases.py", "Database Analysis")
    all_good &= check_file_exists("analysis_tools/check_graph_database.py", "Graph DB Check")
    all_good &= check_file_exists("analysis_tools/debug_retrieval.py", "Retrieval Debug")
    all_good &= check_file_exists("analysis_tools/test_neo4j.py", "Neo4j Testing")
    
    print("\n📦 Data Ingestion:")
    all_good &= check_file_exists("data_ingestion/ingest_rag_apis.py", "API Ingestion")
    all_good &= check_file_exists("data_ingestion/ingest_session1_tutorials.py", "Tutorial Ingestion")
    all_good &= check_file_exists("data_ingestion/populate_neo4j_from_dataset.py", "Neo4j Population")
    all_good &= check_file_exists("data_ingestion/process_documents_to_qdrant.py", "Document Processing")
    
    print("\n💾 Datasets and Dependencies:")
    all_good &= check_file_exists("datasets/requirements.txt", "Python Requirements")
    all_good &= check_file_exists("datasets/test-requirements.txt", "Test Requirements")
    all_good &= check_file_exists("datasets/RAGAPIs.csv", "API Dataset")
    all_good &= check_file_exists("datasets/RAGCodePiece.csv", "Code Examples Dataset")
    all_good &= check_directory_exists("datasets/designs", "Design Files Directory")
    all_good &= check_directory_exists("datasets/platforms", "Platform Files Directory")
    
    print("\n🚀 Setup Scripts:")
    all_good &= check_file_exists("setup_evaluation.sh", "Evaluation Setup Script")
    
    # Check if setup script is executable
    if os.path.exists("setup_evaluation.sh"):
        if os.access("setup_evaluation.sh", os.X_OK):
            print("✅ Setup script is executable")
        else:
            print("⚠️  Setup script exists but is not executable (run: chmod +x setup_evaluation.sh)")
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 VERIFICATION PASSED: All required files are present!")
        print("📋 Package is ready for reviewer evaluation.")
        print("\nNext steps for reviewers:")
        print("1. Run: ./setup_evaluation.sh")
        print("2. Read: README_EVALUATION.md")
        print("3. Check: reports/performance_summary_table.md")
    else:
        print("❌ VERIFICATION FAILED: Some files are missing!")
        print("Please check the missing files listed above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 