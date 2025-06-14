# AGENTE VLSI - OpenROAD RAG Pipeline

A Retrieval-Augmented Generation (RAG) system for VLSI design and OpenROAD that combines vector search with knowledge graphs to provide intelligent code generation and execution.

## Features

- **Dual Database System**: Vector search (Qdrant) + Knowledge graph (Neo4j)
- **AI Code Generation**: Python and Tcl/OpenROAD script generation
- **Code Execution**: Automatic execution with error handling and self-correction
- **Multi-Agent Architecture**: Specialized agents for knowledge extraction and chat
- **Comprehensive Testing**: Unit tests for easy, medium, and hard difficulty levels
- **Performance Validated**: 87% success rate with 34% improvement over baseline LLM

## Prerequisites

- Python 3.8+
- OpenAI API key
- Neo4j Aura account (optional - pipeline works without it)
- OpenROAD (for Tcl code execution)
- ~8GB disk space for databases

## Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
git clone <your-repo>
cd agente_eda
./setup_agente_vlsi.sh
```

The script will:
- ✅ Install Python dependencies
- ✅ Create .env template (you add your OpenAI API key)
- ✅ Initialize vector database (10-15 minutes)
- ✅ Setup Neo4j knowledge graph (optional)
- ✅ Run verification tests
- ✅ Confirm everything is working

### Option 2: Manual Setup

### 1. Clone and Install Dependencies

```bash
git clone <your-repo>
cd agente_eda
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```bash
# Required - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Neo4j Aura credentials (system works without this)
NEO4J_URI=neo4j+s://your_instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

### 3. Initialize Databases (Required for New Installations)

**IMPORTANT**: After cloning, you must populate the databases with the provided data files.

#### Vector Database Setup (Required)
```bash
# Initialize vector database from the provided knowledge base
python add_json_to_qdrant_openai.py

# This will:
# - Create vector_db/ directory
# - Process rag_data.jsonl (7MB, 8000+ entries)
# - Generate embeddings using OpenAI
# - Takes ~10-15 minutes, requires OpenAI API calls
# - Cost: ~$5-10 in OpenAI API credits (one-time setup)
```

**💰 Cost Warning**: Initial setup requires OpenAI API calls to generate embeddings for 8,000+ entries. This typically costs $5-10 in API credits. This is a one-time cost - once created, the vector database can be reused indefinitely.

#### Knowledge Graph Setup (Optional but Recommended)
```bash
# Populate Neo4j with API relationships and code examples
python populate_neo4j_from_dataset.py rag_data.jsonl

# This will:
# - Create 1,679 nodes in Neo4j
# - Establish API relationships
# - Add 384 OpenROAD API functions
# - Requires Neo4j credentials in .env
```

#### Alternative Data Sources
If you need to rebuild from source data:
```bash
# From API documentation (if available)
python ingest_rag_apis.py

# From tutorial files (if available)  
python ingest_session1_tutorials.py

# From markdown documentation (if ORAssistant_RAG_Dataset available)
python process_documents_to_qdrant.py ORAssistant_RAG_Dataset/markdown/
```

#### Verify Database Setup
```bash
# Check vector database
python -c "from pipeline import VLSIRAGPipeline; p = VLSIRAGPipeline(); print('Vector DB ready!')"

# Check Neo4j (if configured)
python check_graph_database.py
```

## Usage

### First Time Setup Verification

Before using the system, verify your databases are properly initialized:

```bash
# Quick test to ensure everything is working
python executor.py "What is the OpenROAD version command?" --no-execute

# If you see a response with Python code, your setup is complete!
# If you get errors about missing databases, run the database setup steps above.
```

### Basic Query

```bash
python executor.py "How do I set up timing constraints in OpenROAD?"
```

### Code Generation

```bash
# Generate Python code
python executor.py "Create a script to read DEF files and analyze timing"

# Generate Tcl/OpenROAD code  
python executor.py "Generate OpenROAD script for global placement"

# Generate code without executing
python executor.py "Create a floorplan script" --no-execute
```

### Advanced Options

```bash
# Adjust retrieval parameters
python executor.py "your query" --top_k 10 --sim_thresh 0.3

# Custom execution timeout
python executor.py "complex routing query" --timeout 120
```

## Testing

### Run All Tests

```bash
# Install test dependencies
pip install -r test-requirements.txt

# Run all tests
pytest

# Run specific test suites
pytest test_executor_easy.py        # Easy Python tests
pytest test_medium_rag_pairs.py     # Medium Python tests  
pytest test_executor_tcl.py         # Tcl/OpenROAD tests
```

### Individual Test Categories

```bash
# Easy tests (basic Python code generation)
python test_executor_easy.py

# Medium tests (file I/O and complex operations)
python test_medium_rag_pairs.py

# Tcl tests (OpenROAD script generation)
python test_executor_tcl.py

# Run single test
python test_executor_tcl.py --test 0  # Run first Tcl test only
```

## Architecture

### Core Pipeline (`pipeline.py`)

The main `VLSIRAGPipeline` class handles:

- **Vector Retrieval**: Semantic search through VLSI documentation using OpenAI embeddings
- **Knowledge Graph**: Neo4j integration for relationship-based context (optional)
- **Multi-Agent System**: KnowledgeGraphAgent + ChatAgent for intelligent responses
- **Code Execution**: Python and Tcl/OpenROAD script execution with error handling

### File Structure

```
agente_eda/
├── pipeline.py                 # Main RAG pipeline
├── executor.py                 # CLI interface for queries
├── vector_db.py               # Vector database utilities
├── test_config.py             # Test configuration
├── test_setup_helper.py       # Test utilities
│
├── rag_data.jsonl             # Main knowledge base (7MB)
├── vector_db/                 # Qdrant vector database (auto-created)
│
├── test_executor_easy.py      # Easy Python tests
├── test_medium_rag_pairs.py   # Medium Python tests  
├── test_executor_tcl.py       # Tcl/OpenROAD tests
│
├── TestSet.xlsx              # Excel test data
├── test_excel_prompts.py     # Excel-based tests
│
└── setup_scripts/            # One-time setup (optional)
    ├── add_json_to_qdrant_openai.py
    ├── populate_neo4j_from_dataset.py
    ├── process_documents_to_qdrant.py
    └── convert_csv_to_jsonl.py
```

## Data Files

### What's Included in the Repository
- ✅ `rag_data.jsonl` - Main knowledge base (7MB, 8,000+ entries)
- ✅ `RAGAPIs.csv` - API documentation (25KB, 193 APIs)  
- ✅ `RAGCodePiece.csv` - Code examples (23KB, 658 examples)
- ✅ `designs/` - OpenROAD design files (gcd.v, etc.)
- ✅ `platforms/` - Technology files (LEF, Liberty)
- ✅ `TestSet.xlsx` - Test cases and validation data
- ✅ All Python scripts and test suites

### What Gets Created During Setup
- ⚠️ `vector_db/` - Vector embeddings database (~2GB, created from rag_data.jsonl)
- ⚠️ `.env` - Your API keys and configuration
- ⚠️ Neo4j database - Knowledge graph (1,679 nodes, optional)

### Core Data (Required)
- `rag_data.jsonl` - Main knowledge base (7MB, 8,000+ entries) ✅ **Included in repo**
- `vector_db/` - Vector embeddings database ⚠️ **Must be created after cloning**
- `RAGAPIs.csv` - API documentation (25KB, 193 APIs) ✅ **Included in repo**
- `RAGCodePiece.csv` - Code examples (23KB, 658 examples) ✅ **Included in repo**

### Test Data  
- `TestSet.xlsx` - Test prompts and expected outputs
- `test_prompts.txt` - Additional test prompts
- `test_prompts_by_difficulty.txt` - Categorized test prompts

### Optional Data
- `RAGCodePiece.csv` - Alternative knowledge base format
- `rag_code_piece.jsonl` - Converted from CSV
- `query_dataset.jsonl` - Alternative knowledge base
- `ORAssistant_RAG_Dataset/` - Source markdown documentation

## Configuration

### Pipeline Configuration

```python
# In your code
from pipeline import VLSIRAGPipeline

pipeline = VLSIRAGPipeline()
response = pipeline.answer_vlsi_query("your question")
```

### Command Line Options

```bash
python executor.py --help

Options:
  --top_k INT          Number of vector search results (default: 7)
  --sim_thresh FLOAT   Similarity threshold (default: 0.2)  
  --no-execute         Generate code but don't execute
  --timeout INT        Code execution timeout in seconds (default: 60)
```

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional Neo4j
NEO4J_URI=neo4j+s://...
NEO4J_USERNAME=neo4j  
NEO4J_PASSWORD=...

# Optional overrides
VECTOR_DB_PATH=vector_db/
COLLECTION_NAME=documents_collection
```

## Troubleshooting

### Database Issues

```bash
# If vector database is missing or corrupted
rm -rf vector_db/
python add_json_to_qdrant_openai.py

# If you get "No vector database found" errors
python add_json_to_qdrant_openai.py

# If Qdrant is locked
ps aux | grep qdrant
kill -9 <PID>

# If Neo4j connection fails
python check_graph_database.py  # Check your .env credentials
```

### First Time Setup Issues

```bash
# If you get "FileNotFoundError: rag_data.jsonl"
# Make sure you're in the correct directory and the file exists
ls -la rag_data.jsonl

# If OpenAI API calls fail during setup
# Check your API key and billing status
python -c "import openai; print('API key configured')"

# If database initialization takes too long
# This is normal - processing 8000+ entries takes 10-15 minutes
# Monitor progress in the terminal output
```

### Test Failures

```bash
# Check OpenROAD installation
which openroad

# Run tests with verbose output
pytest test_executor_tcl.py -v

# Run single failing test
python test_executor_tcl.py --test 0
```

### Performance Issues

```bash
# Use fewer results for faster queries
python executor.py "query" --top_k 3

# Increase similarity threshold for more relevant results  
python executor.py "query" --sim_thresh 0.4
```

## Development

### Adding New Test Cases

1. Add prompts to appropriate test file:
   - `test_executor_easy.py` - Basic Python generation
   - `test_medium_rag_pairs.py` - Complex Python with file I/O
   - `test_executor_tcl.py` - Tcl/OpenROAD scripts

2. Run tests to verify:
   ```bash
   pytest test_file.py -v
   ```

### Extending Knowledge Base

1. Add new documents to `rag_data.jsonl` (JSONL format)
2. Reinitialize vector database:
   ```bash
   rm -rf vector_db/
   python add_json_to_qdrant_openai.py
   ```

### Custom Agents

```python
from pipeline import VLSIRAGPipeline

# Custom configuration
pipeline = VLSIRAGPipeline()
pipeline.config["chat_temperature"] = 0.1  # More deterministic
pipeline.config["top_k"] = 5              # Fewer results

response = pipeline.answer_vlsi_query("your question")
```

## Test Results

The pipeline includes comprehensive test suites:

- **Easy Tests**: Basic Python code generation (pattern matching + execution)
- **Medium Tests**: Complex file I/O operations and analysis  
- **Tcl Tests**: OpenROAD script generation and execution
- **Excel Tests**: Test cases from `TestSet.xlsx`

Run `pytest` to execute all tests and verify system functionality.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for new functionality
4. Ensure all tests pass (`pytest`)
5. Submit a pull request

## License

This project is licensed under the BSD 2-Clause "Simplified" License - see the LICENSE file for details.


            