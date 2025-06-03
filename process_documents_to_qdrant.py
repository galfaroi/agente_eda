import os
import argparse
import json
from typing import List

from dotenv import load_dotenv

from camel.embeddings import OpenAIEmbedding
from camel.types import EmbeddingModelType
from camel.storages import QdrantStorage
from camel.retrievers import VectorRetriever
#from camel.utils import setups_env_vars # For OpenAI API key check
from dotenv import load_dotenv
import os

load_dotenv()



# --- Configuration ---
JSONL_FILE_PATH = "query_dataset.jsonl"  # Your JSONL file
QDRANT_PATH = "vector_db/"
COLLECTION_NAME = "documents_collection"
EMBEDDING_MODEL = "text-embedding-3-large"
OPENAI_BATCH_SIZE = 20
QDRANT_BATCH_SIZE = 100
QDRANT_TEXT_PAYLOAD_KEY = "text"
EMBEDDING_DIMENSION = 3072

# ---------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def find_files(folder_path: str, extensions: List[str]) -> List[str]:
    """Find all files with given extensions in a folder (recursively)."""
    found_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                found_files.append(os.path.join(root, file))
    return found_files


def main():
    parser = argparse.ArgumentParser(
        description="Process markdown and JSON files, chunk, embed, and store in Qdrant."
    )
    parser.add_argument(
        "input_folder", type=str, help="Path to the folder containing .md and .json files."
    )
    parser.add_argument(
        "--qdrant_path",
        type=str,
        default="vector_db",
        help="Path to the local Qdrant storage directory (default: vector_db).",
    )
    parser.add_argument(
        "--qdrant_collection",
        type=str,
        default="documents_collection",
        help="Name of the Qdrant collection (default: documents_collection).",
    )
    parser.add_argument(
        "--embedding_model",
        type=str,
        default=EmbeddingModelType.TEXT_EMBEDDING_3_LARGE,
        help=f"OpenAI embedding model to use (default: {EmbeddingModelType.TEXT_EMBEDDING_3_LARGE})",
    )
    parser.add_argument(
        "--force_reprocess_collection",
        action="store_true",
        help="If set, the existing Qdrant collection will be deleted and recreated."
    )

    args = parser.parse_args()

    print("--- Document Processing and Embedding Script ---")
    print(f"Input folder: {args.input_folder}")
    print(f"Qdrant path: {args.qdrant_path}")
    print(f"Collection: {args.qdrant_collection}")
    print(f"Embedding model: {args.embedding_model}")
    print(f"Force reprocess: {args.force_reprocess_collection}")

    # Check OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in .env file or environment.")
        exit(1)

    # Initialize CAMEL components
    print(f"Initializing embedding model: {args.embedding_model}")
    try:
        embedding_instance = OpenAIEmbedding(model_type=args.embedding_model)
    except Exception as e:
        print(f"Error initializing embedding model: {e}")
        print("Ensure your OpenAI API key is valid and has access to the model.")
        exit(1)

    vector_dim = embedding_instance.get_output_dim()
    print(f"Embedding dimension: {vector_dim}")

    # Handle force reprocess collection
    if args.force_reprocess_collection:
        print(f"Force reprocess enabled. Deleting collection '{args.qdrant_collection}' if it exists at '{args.qdrant_path}'.")
        
        # Delete collection storage directory
        collection_storage_path = os.path.join(args.qdrant_path, "collections", args.qdrant_collection)
        if os.path.exists(collection_storage_path):
            import shutil
            try:
                shutil.rmtree(collection_storage_path)
                print(f"Successfully deleted existing collection data at: {collection_storage_path}")
            except Exception as e:
                print(f"Warning: Could not delete existing collection data at {collection_storage_path}: {e}")
        
        # Clean up collection aliases file
        alias_file_path = os.path.join(args.qdrant_path, "collections_aliases.json")
        if os.path.exists(alias_file_path):
            try:
                with open(alias_file_path, 'r+') as f:
                    aliases = json.load(f)
                    if args.qdrant_collection in aliases.get("aliases", {}):
                        del aliases["aliases"][args.qdrant_collection]
                        f.seek(0)
                        json.dump(aliases, f, indent=4)
                        f.truncate()
                        print(f"Removed alias for '{args.qdrant_collection}' from {alias_file_path}")
            except Exception as e:
                print(f"Warning: Could not update aliases file {alias_file_path}: {e}")

    # Initialize Qdrant storage
    print(f"Initializing Qdrant storage: path='{args.qdrant_path}', collection='{args.qdrant_collection}'")
    try:
        storage_instance = QdrantStorage(
            vector_dim=vector_dim,
            path=args.qdrant_path,
            collection_name=args.qdrant_collection,
        )
        print("✅ Qdrant storage initialized successfully")
    except Exception as e:
        print(f"Error initializing Qdrant storage: {e}")
        exit(1)

    # Initialize vector retriever
    try:
        vector_retriever = VectorRetriever(
            embedding_model=embedding_instance, 
            storage=storage_instance
        )
        print("✅ Vector retriever initialized successfully")
    except Exception as e:
        print(f"Error initializing vector retriever: {e}")
        exit(1)

    # Find and process files
    print(f"Scanning for .md and .json files in: {args.input_folder}")
    
    if not os.path.exists(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' does not exist.")
        exit(1)
    
    files_to_process = find_files(args.input_folder, [".md", ".markdown", ".json"])

    if not files_to_process:
        print("No .md or .json files found in the specified folder.")
        return

    print(f"Found {len(files_to_process)} file(s) to process:")
    for i, file_path in enumerate(files_to_process, 1):
        print(f"  {i}. {file_path}")

    # Process files
    processed_count = 0
    failed_count = 0
    
    for i, file_path in enumerate(files_to_process, 1):
        print(f"\n[{i}/{len(files_to_process)}] Processing: {file_path}")
        try:
            # VectorRetriever.process handles reading, chunking, embedding, and storing
            vector_retriever.process(content=file_path)
            print(f"✅ Successfully processed: {os.path.basename(file_path)}")
            processed_count += 1
        except Exception as e:
            print(f"❌ Error processing file {file_path}: {e}")
            failed_count += 1

    # Summary
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    print(f"Total files found: {len(files_to_process)}")
    print(f"Successfully processed: {processed_count}")
    print(f"Failed to process: {failed_count}")
    print(f"Success rate: {(processed_count/len(files_to_process)*100):.1f}%")
    print(f"Data stored in Qdrant collection '{args.qdrant_collection}' at '{args.qdrant_path}'")
    
    if processed_count > 0:
        print(f"\n✅ Database ready! You can now run queries with:")
        print(f"   python executor.py \"your VLSI question\"")
    
    if failed_count > 0:
        print(f"\n⚠️  {failed_count} files failed to process. Check the error messages above.")


if __name__ == "__main__":
    main()