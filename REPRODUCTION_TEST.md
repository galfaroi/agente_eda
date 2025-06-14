# AGENTE VLSI - Reproduction Test Guide

## Quick Reproduction Test

This guide helps verify that someone can successfully clone and reproduce the AGENTE VLSI system.

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd agente_eda
```

### Step 2: Check Required Files
Verify these essential files are present:
```bash
ls -la rag_data.jsonl          # 7MB knowledge base
ls -la RAGAPIs.csv             # API documentation  
ls -la RAGCodePiece.csv        # Code examples
ls -la setup_agente_vlsi.sh    # Automated setup script
ls -la .env.template           # Environment template
ls -la designs/                # Design files directory
ls -la platforms/              # Technology files directory
```

### Step 3: Setup Environment
```bash
# Copy and configure environment
cp .env.template .env
# Edit .env with your OpenAI API key
```

### Step 4: Run Automated Setup
```bash
./setup_agente_vlsi.sh
```

Expected output:
- ✅ Dependencies installed
- ✅ Vector database created (10-15 minutes)
- ✅ Neo4j setup (optional)
- ✅ Verification tests passed

### Step 5: Test Basic Functionality
```bash
# Test basic query
python executor.py "What is the OpenROAD version command?" --no-execute

# Test code generation
python executor.py "Generate a script to read a DEF file"

# Run test suite
python test_executor_easy.py
```

### Step 6: Verify Performance
```bash
# Check evaluation results
cd evaluation_package
cat reports/performance_summary_table.md
```

Expected results:
- Easy tests: 5/5 (100%)
- Medium tests: 5/5 (100%) 
- Hard tests: 3/5 (60%)
- Overall: 13/15 (87%)

## Troubleshooting

### Common Issues
1. **Missing OpenAI API key**: Update .env file
2. **Vector database creation fails**: Check API key and internet
3. **Neo4j connection fails**: Check credentials or skip (optional)
4. **Test failures**: Check file paths and dependencies

### Success Indicators
- ✅ Vector database created (~2GB in vector_db/)
- ✅ Basic queries return Python/TCL code
- ✅ Test suite shows high success rates
- ✅ No critical errors in setup

## Expected Performance
- **Setup time**: 15-20 minutes (mostly vector DB creation)
- **API cost**: $5-10 for initial setup (one-time)
- **Success rate**: 87% on comprehensive test suite
- **Improvement**: 34% better than baseline LLM

## Files Created During Setup
- `vector_db/` - Vector embeddings database (~2GB)
- `.env` - Your configuration (from template)
- Various log files and temporary outputs

## Repository Completeness Check
✅ Core system files (pipeline.py, executor.py)
✅ Knowledge base (rag_data.jsonl - 7MB)
✅ Test framework (easy/medium/hard tests)
✅ Setup automation (setup_agente_vlsi.sh)
✅ Design files (designs/, platforms/)
✅ Documentation (README.md, evaluation package)
✅ Performance reports and analysis tools

This reproduction test confirms the repository contains everything needed for independent setup and evaluation. 