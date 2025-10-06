import chromadb
import os
from chromadb.utils import embedding_functions # Or adjust import if needed

DB_PATH = 'chroma_db'
COLLECTION_NAME = 'agri_docs'
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2' # Use the same model

db_directory = DB_PATH # Adjust if running from elsewhere
print(f"Connecting to DB at: {os.path.abspath(db_directory)}")

try:
    client = chromadb.PersistentClient(path=db_directory)
    st_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=st_ef)

    print(f"\nAttempting to get first 5 items from collection '{COLLECTION_NAME}'...")
    # Get first 5 items including their metadata
    results = collection.get(limit=5, include=['metadatas'])

    if results and results.get('metadatas'):
        print("\nMetadata of first 5 items:")
        for i, meta in enumerate(results['metadatas']):
            print(f"  Item {i+1}: {meta}")
            if 'summary' not in meta:
                print(f"    >>> WARNING: 'summary' key MISSING in this metadata!")
            elif not meta.get('summary') or meta.get('summary') == '[Snippet Missing]':
                 print(f"    >>> WARNING: 'summary' key found but value is missing or default placeholder!")
    else:
        print("\nCould not retrieve items or metadata from the collection.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    import traceback
    traceback.print_exc()