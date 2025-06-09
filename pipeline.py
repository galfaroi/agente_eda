#!/usr/bin/env python3
"""
RAG Pipeline for VLSI/OpenROAD queries using CAMEL framework - WORKING VERSION
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
        """Initialize the RAG pipeline - EXACT working version."""
        # 1) Load .env
        load_dotenv()
        
        # 2) Embedding + Vector Retriever - Only try OpenAI embedding models
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # make sure this is set
        
        # Only OpenAI embedding models that work with OpenAIEmbedding
        openai_embeddings = ['TEXT_EMBEDDING_3_LARGE', 'TEXT_EMBEDDING_3_SMALL', 'TEXT_EMBEDDING_ADA_2']
        
        print(f"Trying OpenAI embedding models: {openai_embeddings}")
        
        # Try each OpenAI model until one works
        self.embedding = None
        for model_name in openai_embeddings:
            try:
                if hasattr(EmbeddingModelType, model_name):
                    model_type = getattr(EmbeddingModelType, model_name)
                    self.embedding = OpenAIEmbedding(model_type=model_type)
                    print(f"✅ Using embedding model: {model_name}")
                    break
            except Exception as e:
                print(f"⚠️ {model_name} failed: {e}")
                continue
        
        if not self.embedding:
            raise Exception(f"No working OpenAI embedding model found!")
        
        self.vector_store = QdrantStorage(
            vector_dim=self.embedding.get_output_dim(),
            path="vector_db/",
            collection_name="documents_collection",
        )
        self.vector_retriever = VectorRetriever(
            embedding_model=self.embedding,
            storage=self.vector_store,
        )
        
        # 3) Knowledge-Graph Storage (Neo4j)
        self.n4j = Neo4jGraph(
            url="neo4j+s://a77d863c.databases.neo4j.io",
            username="neo4j",
            password="f1zopPMnKXlhQAYvugcoLUr8t0s9QruIyYsY0YxBBhU"
        )
        
        # 4) Unstructured IO & KG‐Agent
        self.uio = UnstructuredIO()
        
        # 5) OpenAI Chat Model - Only try GPT models
        # Only GPT models that work
        gpt_models = ['GPT_4O_MINI', 'GPT_4O', 'GPT_4', 'GPT_3_5_TURBO']
        
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
        
        # 6) KG Agent
        self.kg_agent = KnowledgeGraphAgent(model=self.openai_model)
        
        # 7) System prompt for ChatAgent
        sys_msg = BaseMessage.make_assistant_message(
            role_name="VLSI Engineer",
            content=(
                "You are a VLSI design automation expert specializing in the RTL-to-GDSII flow.\n"
                "Your job has three modes, depending on the user's request:\n\n"
                "1) Python Script Generation Mode\n"
                "   - When the user asks for Python code or mentions Python explicitly\n"
                "   - Start every script with exactly:\n"
                "     import openroad\n"
                "   - Never use `from openroad import …` or any alias—use only the top-level `openroad` namespace\n"
               # "   - Use only snake_case module-level calls with these exact variable names:\n"
                "   -user may ask for just the script but no execution dont fence in a python block"
                "   - Wrap the entire script in a single fenced python block:\n"
                "     ```python\n"
                "     # your code here\n"
                "   - Do not emit any prose or explanations—only the runnable script.\n\n"
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
        
        print("✅ Pipeline initialized successfully")
    
    def query(self, query: str, top_k: int = 7, similarity_threshold: float = 0.2) -> str:
        """
        1) Vector‐based retrieval
        2) KG extraction & Neo4j lookups
        3) Combine contexts and ask camel_agent
        4) Return the assistant's first message
        """
        # Vector retrieval
        retrieved = self.vector_retriever.query(
            query=query,
            top_k=top_k,
            similarity_threshold=similarity_threshold
        )

        # KG‐agent extraction
        el = self.uio.create_element_from_text(text=query, element_id="kg_query")
        ans_el = self.kg_agent.run(el, parse_graph_elements=True)

        # Neo4j lookups
        kg_ctx = []
        for node in ans_el.nodes:
            cypher = f"""
            MATCH (n {{id: '{node.id}'}})-[r]->(m)
            RETURN 'Node ' + n.id + ' --' + type(r) + '--> ' + m.id AS desc
            UNION
            MATCH (n)<-[r]-(m {{id: '{node.id}'}})
            RETURN 'Node ' + m.id + ' --' + type(r) + '--> ' + n.id AS desc
            """
            for rec in self.n4j.query(query=cypher):
                kg_ctx.append(rec["desc"])

        # Combine contexts
        context = f"{retrieved}\n" + "\n".join(kg_ctx)

        # Ask the agent
        user_msg = BaseMessage.make_user_message(
            role_name="vlsi User",
            content=f"The Original Query is: {query}\n\nRetrieved Context:\n{context}"
        )
        resp = self.camel_agent.step(user_msg)
        return resp.msgs[0].content


# Convenience function for backward compatibility
def answer_vlsi_query(query: str, top_k: int = 7, similarity_threshold: float = 0.2) -> str:
    """Backward compatibility function."""
    pipeline = VLSIRAGPipeline()
    return pipeline.query(query, top_k, similarity_threshold)