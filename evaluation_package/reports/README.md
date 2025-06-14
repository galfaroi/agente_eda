# VLSI RAG Pipeline

A Retrieval-Augmented Generation (RAG) system for VLSI design and OpenROAD that combines vector search with knowledge graphs to provide intelligent code generation and execution.

## Features

- **Dual Database System**: Vector search (Qdrant) + Knowledge graph (Neo4j)
- **AI Code Generation**: Python and Tcl/OpenROAD script generation
- **Code Execution**: Automatic execution with error handling and self-correction
- **Multi-Agent Architecture**: Specialized agents for knowledge extraction and chat
- **Comprehensive Testing**: Unit tests for easy, medium, and Tcl code generation

## Prerequisites

- Python 3.8+
- OpenAI API key
- Neo4j Aura account (optional - pipeline works without it)
- OpenROAD (for Tcl code execution)

## Quick Setup

### 1. Clone and Install Dependencies

```bash
git clone <your-repo>
cd agente_eda
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Neo4j (pipeline works without this)
NEO4J_URI=neo4j+s://your_instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

### 3. Initialize Vector Database (One-time)

The vector database is pre-populated with `rag_data.jsonl`. If you need to reinitialize:

```bash
# Option 1: Use the existing JSONL directly
python add_json_to_qdrant_openai.py  # Only if vector_db/ is missing

# Option 2: Process from markdown sources (if you have ORAssistant_RAG_Dataset)
python process_documents_to_qdrant.py ORAssistant_RAG_Dataset/markdown/
```

### 4. (Optional) Initialize Knowledge Graph

```bash
python populate_neo4j_from_dataset.py rag_data.jsonl
```

## Usage

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

### Core Data (Required)
- `rag_data.jsonl` - Main knowledge base (7MB, 8,000+ entries)
- `vector_db/` - Vector embeddings database (auto-created from rag_data.jsonl)

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
# If vector database is corrupted
rm -rf vector_db/
python add_json_to_qdrant_openai.py

# If Qdrant is locked
ps aux | grep qdrant
kill -9 <PID>
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


            