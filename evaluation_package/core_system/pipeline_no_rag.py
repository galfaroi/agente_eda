#!/usr/bin/env python3
"""
RAG Pipeline for VLSI/OpenROAD queries using CAMEL framework - NO RAG VERSION (Ablation Study)
This version disables both vector database and Neo4j graph database to test baseline LLM performance.
"""
import os
from dotenv import load_dotenv

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType, EmbeddingModelType
from camel.configs import ChatGPTConfig
from camel.embeddings import OpenAIEmbedding
from camel.storages import QdrantStorage, Neo4jGraph
from camel.retrievers import VectorRetriever
from camel.loaders import UnstructuredIO
from camel.agents import KnowledgeGraphAgent, ChatAgent
from camel.messages import BaseMessage

class VLSIRAGPipeline:
    def __init__(self):
        """Initialize the RAG pipeline - NO RAG VERSION for ablation study."""
        # 1) Load .env
        load_dotenv()
        
        # Skip embedding and vector store setup for ablation
        print("🚫 Skipping vector database setup (ablation study)")
        self.embedding = None
        self.vector_store = None
        self.vector_retriever = None
        
        # Skip Neo4j setup for ablation
        print("🚫 Skipping Neo4j graph database setup (ablation study)")
        self.n4j = None
        
        # Skip KG agent setup for ablation
        print("🚫 Skipping Knowledge Graph agent setup (ablation study)")
        self.uio = None
        self.kg_agent = None
        
        # 5) OpenAI Chat Model - Only try GPT models (latest first)
        # Only GPT models that work - prioritizing newest and most capable
        gpt_models = ['GPT_4_1', 'O1', 'GPT_4O', 'GPT_4O_MINI', 'GPT_4', 'GPT_3_5_TURBO']
        
        print(f"Trying GPT models: {gpt_models}")
        
        # Try .as_dict() first, fallback to manual dict
        try:
            chat_cfg = ChatGPTConfig(temperature=0.2).as_dict()
        except:
            chat_cfg = {'temperature': 0.2}
        
        # Try GPT models until one works
        self.openai_model = None
        for model_name in gpt_models:
            try:
                if hasattr(ModelType, model_name):
                    model_type = getattr(ModelType, model_name)
                    self.openai_model = ModelFactory.create(
                        model_platform=ModelPlatformType.OPENAI,
                        model_type=model_type,
                        model_config_dict=chat_cfg,
                    )
                    print(f"✅ Using GPT model: {model_name}")
                    break
            except Exception as e:
                print(f"⚠️ {model_name} failed: {e}")
                continue
        
        if not self.openai_model:
            raise Exception(f"No working GPT model found!")
        
        # 7) System prompt for ChatAgent
        sys_msg = BaseMessage.make_assistant_message(
            role_name="VLSI Engineer",
            content=(
                "You are a VLSI design automation expert specializing in the RTL-to-GDSII flow.\n"
                "Your job has three modes, depending on the user's request:\n\n"
                "1) Python Script Generation Mode\n"
                "   - When the user asks for Python code or mentions Python explicitly\n"
                "   - CRITICAL: Start every script with exactly 'import openroad' (no variations)\n"
                "   - NEVER use 'from openroad import ...' or any aliases\n"
                "   - Use EXACT patterns: tech = openroad.Tech(), design = openroad.Design(tech)\n"
                "   - Use EXACT method names: tech.readLiberty(), tech.readLef(), design.readVerilog(), design.link()\n"
                "   - MANDATORY: For Verilog/DEF operations, ALWAYS load technology files first to prevent crashes\n"
                "   - NEVER read design files (Verilog/DEF) without loading Liberty and LEF files first\n"
                "   - Follow this EXACT structure for common tasks:\n"
                "     * Liberty: tech = openroad.Tech(); tech.readLiberty(path)\n"
                "     * LEF: tech = openroad.Tech(); tech.readLef(path)\n"
                "     * Verilog: tech = openroad.Tech(); tech.readLiberty('platforms/lib/NangateOpenCellLibrary_typical.lib'); tech.readLef('platforms/lef/NangateOpenCellLibrary.tech.lef'); design = openroad.Design(tech); design.readVerilog(path); design.link(module)\n"
                "     * DEF: tech = openroad.Tech(); tech.readLiberty('platforms/lib/NangateOpenCellLibrary_typical.lib'); tech.readLef('platforms/lef/NangateOpenCellLibrary.tech.lef'); design = openroad.Design(tech); design.readDef(path)\n"
                "     * ODB: tech = openroad.Tech(); design = openroad.Design(tech); design.readDb(path)\n"
                "   - Wrap in single fenced python block: ```python\\n# code\\n```\n"
                "   - Generate ONLY executable code, no explanations.\n\n"
                "2) Tcl Script Generation Mode\n"
                "   - When user asks for Tcl code, mentions Tcl, or requests generic OpenROAD scripts\n"
                "   - Produce a single, self-contained ```tcl``` script for OpenROAD\n"
                "   - Use native OpenROAD Tcl commands (read_lef, read_def, place_design, etc.)\n"
                "   - Include proper error handling with Tcl syntax\n"
                "   - Wrap the entire script in one fenced code block:\n"
                "     ```tcl\n"
                "     # your code here\n"
                "     ```\n"
                "   - Do not emit any prose, explanations, or extra text—only the runnable script.\n\n"
                "3) VLSI Q&A Mode\n"
                "   - If the user asks a question about VLSI design, physical implementation,\n"
                "     timing, power, constraints, or OpenROAD usage, provide a concise,\n"
                "     accurate technical explanation.\n"
                "   - You may include small code snippets in Python or Tcl to illustrate your answer,\n"
                "     but keep them minimal and relevant.\n"
                "   - Precede code examples with a brief introduction in plain text,\n"
                "     and present them in fenced blocks with proper language tags.\n\n"
                "Language Selection Guidelines:\n"
                "- Default to Tcl for generic OpenROAD requests (Tcl is OpenROAD's native language)\n"
                "- Use Python only when explicitly requested or when complex data processing is needed\n"
                "- For simple OpenROAD commands (read files, run tools), prefer Tcl\n"
                "- For complex algorithms or data analysis, prefer Python\n\n"
                "Choose the appropriate mode automatically and respond accordingly."
            )
        )
        
        # 8) ChatAgent
        self.camel_agent = ChatAgent(system_message=sys_msg, model=self.openai_model)
        
        print("✅ Pipeline initialized successfully (NO RAG - Baseline LLM only)")
    
    def query(self, query: str, top_k: int = 7, similarity_threshold: float = 0.2) -> str:
        """
        NO RAG VERSION: Skip all retrieval and directly query the LLM.
        This tests baseline LLM performance without any external knowledge.
        """
        print("🚫 Skipping vector retrieval (ablation study)")
        print("🚫 Skipping knowledge graph extraction (ablation study)")
        print("🚫 Skipping Neo4j lookups (ablation study)")
        
        # Ask the agent directly without any context
        user_msg = BaseMessage.make_user_message(
            role_name="vlsi User",
            content=f"The Original Query is: {query}\n\nNo external context available (baseline LLM test)."
        )
        resp = self.camel_agent.step(user_msg)
        return resp.msgs[0].content


# Convenience function for backward compatibility
def create_vlsi_rag_pipeline():
    """Create and return a VLSIRAGPipeline instance."""
    return VLSIRAGPipeline()

if __name__ == "__main__":
    # Test the pipeline
    pipeline = VLSIRAGPipeline()
    
    # Test query
    test_query = "Write Python code to get OpenROAD version using openroad_version()"
    print(f"\nTest Query: {test_query}")
    print("=" * 50)
    
    response = pipeline.query(test_query)
    print(f"Response: {response}") 