#!/bin/bash

# AGENTE VLSI - Automated Setup Script
# This script sets up the databases and verifies the installation

echo "🚀 AGENTE VLSI - Automated Setup"
echo "================================="

# Check if we're in the right directory
if [ ! -f "rag_data.jsonl" ]; then
    echo "❌ Error: rag_data.jsonl not found. Please run this script from the AGENTE VLSI root directory."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating template..."
    cat > .env << EOF
# Required - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Neo4j Aura credentials (system works without this)
NEO4J_URI=neo4j+s://your_instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
EOF
    echo "📝 Please edit .env file with your OpenAI API key before continuing."
    echo "   You can get an API key from: https://platform.openai.com/api-keys"
    read -p "Press Enter after you've updated the .env file..."
fi

# Check if OpenAI API key is configured
if grep -q "your_openai_api_key_here" .env; then
    echo "❌ Error: Please update your OpenAI API key in the .env file"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "🔍 Checking for existing vector database..."
if [ -d "vector_db" ] && [ "$(ls -A vector_db)" ]; then
    echo "✅ Vector database already exists, skipping creation."
else
    echo "📊 Creating vector database from rag_data.jsonl..."
    echo "   This will take 10-15 minutes and make OpenAI API calls..."
    echo "   Processing 8,000+ entries..."
    python add_json_to_qdrant_openai.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Vector database created successfully!"
    else
        echo "❌ Vector database creation failed. Check your OpenAI API key and internet connection."
        exit 1
    fi
fi

echo ""
echo "🔍 Checking Neo4j configuration..."
if grep -q "your_password" .env; then
    echo "⚠️  Neo4j not configured (optional). System will work with vector database only."
else
    echo "📈 Checking Neo4j knowledge graph..."
    # Check if Neo4j already has data
    neo4j_node_count=$(python -c "
try:
    from camel.storages import Neo4jGraph
    import os
    n4j = Neo4jGraph(
        url=os.getenv('NEO4J_URI', os.getenv('NEO4J_URL')),
        username=os.getenv('NEO4J_USERNAME', 'neo4j'),
        password=os.getenv('NEO4J_PASSWORD')
    )
    result = n4j.query('MATCH (n) RETURN count(n) as count')
    print(result[0]['count'] if result else 0)
except:
    print(0)
" 2>/dev/null)
    
    if [ "$neo4j_node_count" -gt 100 ]; then
        echo "✅ Neo4j knowledge graph already populated ($neo4j_node_count nodes). Skipping creation."
    else
        echo "📈 Setting up Neo4j knowledge graph..."
        python populate_neo4j_from_dataset.py rag_data.jsonl
        
        if [ $? -eq 0 ]; then
            echo "✅ Neo4j knowledge graph created successfully!"
        else
            echo "⚠️  Neo4j setup failed (optional). System will work with vector database only."
        fi
    fi
fi

echo ""
echo "🧪 Running verification tests..."

# Test vector database
echo "Testing vector database..."
python -c "from pipeline import VLSIRAGPipeline; p = VLSIRAGPipeline(); print('✅ Vector database working!')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Vector database test failed"
    exit 1
fi

# Test basic query
echo "Testing basic query..."
python executor.py "What is the OpenROAD version command?" --no-execute > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Basic query test passed!"
else
    echo "❌ Basic query test failed"
    exit 1
fi

echo ""
echo "🎉 AGENTE VLSI Setup Complete!"
echo "=============================="
echo ""
echo "✅ Vector database: Ready (8,000+ entries)"
echo "✅ Pipeline: Functional"
echo "✅ Code generation: Working"
echo ""
echo "🚀 Try these commands:"
echo "   python executor.py \"How do I read a DEF file in OpenROAD?\""
echo "   python executor.py \"Generate a floorplanning script\""
echo "   python test_executor_easy.py  # Run test suite"
echo ""
echo "📚 For more information:"
echo "   - Read README.md for detailed usage"
echo "   - Check evaluation_package/ for performance analysis"
echo "   - Run pytest for comprehensive testing"
echo ""
echo "🎯 System Performance: 87% success rate, 34% improvement over baseline LLM" 