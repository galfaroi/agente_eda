# AGENTE VLSI - Evaluation Package

## Overview

This evaluation package contains AGENTE VLSI, a complete OpenROAD RAG (Retrieval-Augmented Generation) system for automated Python code generation in VLSI/EDA workflows. The system combines vector databases, graph databases, and large language models to generate contextually accurate OpenROAD Python code.

## 📁 Directory Structure

```
evaluation_package/
├── README_EVALUATION.md          # This file - evaluation guide
├── core_system/                  # Main system components
│   ├── pipeline.py              # Full RAG pipeline (Vector DB + Neo4j + LLM)
│   ├── pipeline_no_rag.py       # Baseline LLM-only pipeline (for ablation)
│   └── executor.py              # Code execution and validation engine
├── test_suites/                 # Comprehensive test framework
│   ├── easy/                    # Basic API tests (5 tests)
│   │   ├── test_easy_rag_pairs.py
│   │   └── test_executor_easy.py
│   ├── medium/                  # File loading tests (5 tests)
│   │   └── test_medium_rag_pairs.py
│   ├── hard/                    # Complex workflow tests (5 tests)
│   │   ├── test_hard_rag_pairs.py
│   │   └── test_executor_hard_new.py
│   └── ablation_studies/        # No-RAG comparison tests
│       ├── test_executor_easy_no_rag.py
│       └── test_executor_hard_no_rag.py
├── data_ingestion/              # Knowledge base creation scripts
│   ├── ingest_rag_apis.py       # Vector database ingestion
│   ├── ingest_session1_tutorials.py  # Tutorial ingestion
│   ├── populate_neo4j_from_dataset.py  # Graph database creation
│   └── process_documents_to_qdrant.py  # Document processing
├── analysis_tools/              # Debugging and analysis utilities
│   ├── analyze_rag_databases.py # Database content analysis
│   ├── check_graph_database.py  # Neo4j validation
│   ├── debug_retrieval.py       # Retrieval debugging
│   └── test_neo4j.py           # Graph database testing
├── reports/                     # Performance analysis and documentation
│   ├── agent_performance_report.md     # Comprehensive performance analysis
│   ├── performance_summary_table.md   # Quick results summary
│   └── README.md               # Original project documentation
└── datasets/                   # Test data and requirements
    ├── designs/                # OpenROAD design files (gcd.v, etc.)
    ├── platforms/              # Technology files (LEF, Liberty)
    ├── RAGAPIs.csv            # API documentation dataset
    ├── RAGCodePiece.csv       # Code examples dataset
    ├── requirements.txt        # Python dependencies
    └── test-requirements.txt   # Test-specific dependencies
```

## 🚀 Quick Start for Reviewers

### 1. Environment Setup
```bash
cd evaluation_package
pip install -r datasets/requirements.txt
pip install -r datasets/test-requirements.txt
```

### 2. Run Performance Tests
```bash
# Test the full RAG system
cd test_suites/easy && python test_executor_easy.py
cd ../hard && python test_executor_hard_new.py -d medium
cd ../hard && python test_executor_hard_new.py -d hard

# Test the baseline (no RAG) system for comparison
cd ../ablation_studies && python test_executor_easy_no_rag.py
cd ../ablation_studies && python test_executor_hard_no_rag.py -d medium
cd ../ablation_studies && python test_executor_hard_no_rag.py -d hard
```

### 3. View Results
```bash
cd reports/
cat performance_summary_table.md    # Quick results overview
cat agent_performance_report.md     # Detailed analysis
```

## 📊 Key Performance Results

| Test Category | RAG System | No RAG (Baseline) | Improvement |
|---------------|------------|-------------------|-------------|
| **Easy Tests** | 5/5 (100%) | 5/5 (100%) | 0% |
| **Medium Tests** | 5/5 (100%) | 2/5 (40%) | **+60%** |
| **Hard Tests** | 3/5 (60%) | 1/5 (20%) | **+40%** |
| **Overall** | **13/15 (87%)** | **8/15 (53%)** | **+34%** |

## 🔍 System Architecture

### RAG Pipeline Components
1. **Vector Database (Qdrant)**: Stores 3,072 OpenROAD documentation embeddings
2. **Graph Database (Neo4j)**: Contains 1,679 nodes with API relationships
3. **LLM (GPT-4.1)**: Generates code using retrieved context
4. **Executor**: Validates and runs generated Python code

### Test Framework
- **Easy Tests**: Basic API calls (`openroad_version()`, `db_has_tech()`)
- **Medium Tests**: File loading (Liberty, LEF, Verilog, DEF, ODB)
- **Hard Tests**: Complete workflows (floorplanning, placement, routing)

## 🧪 Evaluation Methodology

### Test Validation Criteria
1. **Code Structure**: Python syntax, imports, basic structure
2. **API Patterns**: Correct OpenROAD API usage patterns
3. **Execution Success**: Code runs without errors
4. **Functional Correctness**: Achieves intended VLSI workflow goals

### Ablation Study Design
- **Full RAG**: Vector DB + Graph DB + LLM
- **No RAG**: LLM only (no external knowledge retrieval)
- **Comparison**: Direct performance comparison across difficulty levels

## 📈 Key Findings

### RAG System Advantages
1. **Complex Workflow Generation**: 60% better on medium complexity tasks
2. **API Pattern Accuracy**: Correctly uses OpenROAD-specific patterns
3. **File Path Resolution**: Automatically uses correct design/platform files
4. **Contextual Code Generation**: Leverages domain-specific knowledge

### Baseline LLM Limitations
1. **Generic Code Generation**: Produces syntactically correct but functionally incorrect code
2. **Missing Domain Knowledge**: Lacks OpenROAD-specific patterns
3. **File Path Errors**: Uses non-existent file paths
4. **API Misuse**: Incorrect parameter usage and function calls

## 🔧 Technical Implementation

### Core Technologies
- **CAMEL Framework**: Multi-agent RAG orchestration
- **Qdrant**: Vector similarity search
- **Neo4j**: Graph-based knowledge representation
- **OpenAI GPT-4.1**: Code generation
- **OpenROAD**: Target VLSI tool integration

### Knowledge Base Content
- **3,072 Vector Embeddings**: OpenROAD documentation and tutorials
- **1,679 Graph Nodes**: API functions, parameters, relationships
- **384 OpenROAD APIs**: Comprehensive function coverage
- **Real Design Files**: Actual VLSI designs for testing

## 📝 Reproduction Instructions

### For Complete Evaluation
1. **Setup Environment**: Install dependencies from `datasets/requirements.txt`
2. **Run All Tests**: Execute test suites in order (easy → medium → hard)
3. **Compare Results**: Run both RAG and no-RAG versions
4. **Analyze Performance**: Review generated reports in `reports/`

### For Individual Component Testing
- **Vector DB Analysis**: Use `analysis_tools/analyze_rag_databases.py`
- **Graph DB Validation**: Use `analysis_tools/check_graph_database.py`
- **Retrieval Debugging**: Use `analysis_tools/debug_retrieval.py`

## 🎯 Evaluation Criteria for Reviewers

### System Performance (40%)
- Code generation accuracy across difficulty levels
- Execution success rates
- API pattern correctness

### Technical Innovation (30%)
- RAG architecture design
- Multi-modal knowledge integration (vector + graph)
- Domain-specific optimization

### Experimental Rigor (20%)
- Comprehensive ablation studies
- Systematic test framework
- Reproducible results

### Practical Impact (10%)
- Real-world applicability
- VLSI workflow coverage
- Tool integration quality

## 📞 Support Information

For questions about the evaluation:
1. Check `reports/agent_performance_report.md` for detailed analysis
2. Review test outputs in respective test suite directories
3. Use analysis tools for deeper investigation
4. Refer to original `README.md` for system background

---

**Note**: This evaluation package represents a complete, self-contained system for assessing AGENTE VLSI performance. All necessary files, data, and instructions are included for independent evaluation. 