#!/bin/bash

# AGENTE VLSI - Evaluation Setup Script
# This script sets up the environment and runs basic validation tests

echo "🚀 AGENTE VLSI Evaluation Setup"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "README_EVALUATION.md" ]; then
    echo "❌ Error: Please run this script from the evaluation_package directory"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip install -r datasets/requirements.txt
pip install -r datasets/test-requirements.txt

echo ""
echo "🧪 Running quick validation tests..."
echo ""

# Test easy suite
echo "Testing Easy Suite (RAG System)..."
cd test_suites/easy
python test_executor_easy.py > ../../easy_rag_results.txt 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Easy tests (RAG) completed successfully"
else
    echo "⚠️  Easy tests (RAG) had some issues - check easy_rag_results.txt"
fi
cd ../..

# Test medium suite
echo "Testing Medium Suite (RAG System)..."
cd test_suites/hard
python test_executor_hard_new.py -d medium > ../../medium_rag_results.txt 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Medium tests (RAG) completed successfully"
else
    echo "⚠️  Medium tests (RAG) had some issues - check medium_rag_results.txt"
fi
cd ../..

# Test hard suite
echo "Testing Hard Suite (RAG System)..."
cd test_suites/hard
python test_executor_hard_new.py -d hard > ../../hard_rag_results.txt 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Hard tests (RAG) completed successfully"
else
    echo "⚠️  Hard tests (RAG) had some issues - check hard_rag_results.txt"
fi
cd ../..

echo ""
echo "📊 Evaluation setup complete!"
echo ""
echo "Next steps:"
echo "1. Review test results in *_results.txt files"
echo "2. Check reports/performance_summary_table.md for quick overview"
echo "3. Read reports/agent_performance_report.md for detailed analysis"
echo "4. Run ablation studies: cd test_suites/ablation_studies && python test_executor_easy_no_rag.py"
echo ""
echo "For detailed instructions, see README_EVALUATION.md" 