# AGENTE VLSI RAG Pipeline

A Retrieval-Augmented Generation (RAG) system for VLSI design and OpenROAD, combining vector search with knowledge graphs to provide intelligent code generation and execution.

## Features

- **Vector Search**: Semantic search through VLSI documentation using OpenAI embeddings
- **Knowledge Graph**: Neo4j integration for relationship-based context retrieval
- **Code Generation**: AI-powered Python/OpenROAD script generation
- **Code Execution**: Automatic execution with OpenROAD or standard Python
- **Self-Correction**: AI analyzes execution errors and provides fixes
- **Clean Architecture**: Modular design with proper resource management
- **Multi-Agent System**: Specialized AI agents for different tasks

## Prerequisites

- Python 3.8+
- OpenAI API key
- Neo4j Aura account (or local Neo4j instance)
- OpenROAD 

## Installation

1. **Clone and setup environment:**
   ```bash
   git clone <your-repo>
   cd vlsi-rag-pipeline
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env with your credentials:
   OPENAI_API_KEY=your_openai_api_key_here
   NEO4J_URI=neo4j+s://your_neo4j_instance.databases.neo4j.io
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_neo4j_password
   ```

3. **Install OpenROAD **
  https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts

## Quick Start

### 1. Initialize Database (One-time setup)

```bash
# Populate vector database with your VLSI documents
python init_qdrant.py
```

This reads `query_dataset.jsonl` and creates embeddings in the `vector_db/` directory.

### 2. Run Queries

```bash
# Basic query
python executor.py "How do I set up timing constraints in OpenROAD?"

# Query with custom parameters
python executor.py "Generate a floorplan script" --top_k 10 --sim_thresh 0.3

# Generate code without executing
python executor.py "Create a placement script" --no-execute

# Custom execution timeout
python executor.py "Run detailed routing" --timeout 120
```

### 3. Interactive Mode

```bash
# Keep pipeline loaded for faster repeated queries
python interactive_vlsi.py
```

## Usage Examples

### Basic VLSI Questions
```bash
python executor.py "What is IR drop analysis?"
python executor.py "Explain clock tree synthesis"
python executor.py "How does placement optimization work?"
```

### Code Generation
```bash
python executor.py "Generate a script to read a DEF file"
python executor.py "Create a timing analysis script"
python executor.py "Write code to extract net delays"
```

### OpenROAD-Specific
```bash
python executor.py "Initialize OpenROAD design and read LEF/DEF"
python executor.py "Run global placement with OpenROAD"
python executor.py "Generate OpenROAD routing script"
```

## Architecture

### Core Components

- **`pipeline.py`**: Main RAG pipeline with lazy-loaded components
- **`executor.py`**: Query execution and code running interface
- **`init_qdrant.py`**: One-time database initialization
- **`test_neo4j.py`**: Neo4j connection testing utility

### Multi-Agent System

The pipeline uses **2 specialized CAMEL agents** that work together:

#### 1. KnowledgeGraphAgent
```python
@property
def kg_agent(self) -> KnowledgeGraphAgent:
    """Lazy initialization of knowledge graph agent."""
    if self._kg_agent is None:
        self._kg_agent = KnowledgeGraphAgent()
    return self._kg_agent
```

- **Purpose**: Extracts entities and relationships from VLSI queries
- **Function**: Parses user queries to identify VLSI concepts, components, and relationships
- **Used in**: `_get_kg_context()` method for Neo4j knowledge graph lookups
- **Example**: Query "How does placement affect timing?" → Extracts entities: ["placement", "timing", "optimization"]

#### 2. ChatAgent
```python
@property
def chat_agent(self) -> ChatAgent:
    """Lazy initialization of chat agent."""
    if self._chat_agent is None:
        model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=self.config["chat_model"],
            model_config_dict=ChatGPTConfig(
                temperature=self.config["chat_temperature"]
            ).as_dict(),
        )
        self._chat_agent = ChatAgent(model)
    return self._chat_agent
```

- **Purpose**: Main conversational AI for response and code generation
- **Function**: Combines retrieved context to generate intelligent responses and executable code
- **Used in**: `answer_vlsi_query()` method for final response generation
- **Features**: Temperature-controlled responses, context-aware code generation

### Agent Workflow

```
User Query: "Generate OpenROAD placement script"
    ↓
KnowledgeGraphAgent → Extracts: ["OpenROAD", "placement", "script"]
    ↓                    ↓
    ↓               Neo4j Lookup → Finds relationships: placement→timing, placement→floorplan
    ↓
Vector Retrieval → Gets relevant documentation about OpenROAD placement
    ↓
ChatAgent → Combines context → Generates Python/OpenROAD code
    ↓
Code Execution → Runs with OpenROAD or Python
    ↓
Self-Correction → If errors, ChatAgent analyzes and fixes code
```

### Data Flow

1. **Query Processing**: User query → KnowledgeGraphAgent extracts entities → Vector search + Knowledge graph lookup
2. **Context Retrieval**: Relevant documents and relationships retrieved from both sources
3. **Response Generation**: ChatAgent generates response with combined context
4. **Code Execution**: If code detected → Execute with OpenROAD/Python
5. **Error Handling**: If execution fails → ChatAgent provides corrections

### Database Structure

```
vector_db/                 # Qdrant vector database
├── collection.json        # Collection metadata
├── storage/               # Vector storage
└── .qdrant_lock          # Lock file (auto-managed)

query_dataset.jsonl        # Source documents (JSONL format)
```

## Configuration

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
OPENAI_API_KEY=sk-...                    # OpenAI API key

# Neo4j (optional - will work without)
NEO4J_URI=neo4j+s://...                  # Neo4j connection string
NEO4J_USERNAME=neo4j                     # Neo4j username
NEO4J_PASSWORD=...                       # Neo4j password

# Optional overrides
VECTOR_DB_PATH=vector_db/                # Vector database path
COLLECTION_NAME=documents_collection      # Qdrant collection name
```

### Agent Configuration

Both agents are **lazily loaded** (created only when first used) and **reused** across multiple queries for efficiency:

```python
# Custom agent configuration
config = {
    "chat_temperature": 0.1,     # More deterministic ChatAgent responses
    "chat_model": ModelType.GPT_4O_MINI,  # Model for ChatAgent
}

pipeline = VLSIPipeline(config)
```

## Troubleshooting

### Database Issues

```bash
# If Qdrant database is locked
ps aux | grep qdrant
kill -9 <PID>

# Recreate database
rm -rf vector_db/
python init_qdrant.py
```

### Neo4j Connection

```bash
# Test Neo4j connection
python test_neo4j.py

# Pipeline works without Neo4j if connection fails
# Check logs for "Continuing without Neo4j..."
```

### Code Execution

```bash
# Test OpenROAD availability
which openroad

# Run without code execution
python executor.py "your query" --no-execute

# Check execution logs for timeout/error details
```

### Performance Issues

```bash
# Use smaller result sets for faster queries
python executor.py "query" --top_k 3

# Increase similarity threshold to get more relevant results
python executor.py "query" --sim_thresh 0.4
```

## Development

### Adding New Documents

1. Add documents to `query_dataset.jsonl` (one JSON object per line)
2. Run `python init_qdrant.py` to rebuild the database

### Extending the Pipeline

```python
# Custom configuration
from pipeline import VLSIPipeline

config = {
    "chat_temperature": 0.1,  # More deterministic
    "top_k": 5,              # Fewer results
}

pipeline = VLSIPipeline(config)
response = pipeline.answer_vlsi_query("your question")
```

### Testing Components

```python
# Test individual components
python test_neo4j.py           # Neo4j connection
python inspect_qdrant.py       # Vector database inspection
```

## File Structure

```
vlsi-rag-pipeline/
├── pipeline.py              # Main RAG pipeline with multi-agent system
├── executor.py              # CLI interface and code execution
├── init_qdrant.py           # Database initialization
├── test_neo4j.py           # Neo4j testing utility
├── inspect_qdrant.py       # Database inspection tool
├── interactive_vlsi.py     # Interactive query interface
├── query_dataset.jsonl     # Source documents
├── vector_db/              # Vector database (auto-created)
├── .env                    # Environment configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

BSD 2-Clause "Simplified" License


            