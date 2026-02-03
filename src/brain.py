import chromadb
from chromadb.utils import embedding_functions

class ScisneBrain:
    """
    Vector Database manager using ChromaDB.
    Stores technical schema combined with human-friendly business logic.
    """
    def __init__(self, storage_path="./scisne_memory"):
        # Local embedding model (Small and efficient)
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.client = chromadb.PersistentClient(path=storage_path)
        
        # Initialize or retrieve collection
        self.collection = self.client.get_or_create_collection(
            name="business_context", 
            embedding_function=self.emb_fn
        )

    def learn(self, table_name, raw_schema, description, column_metadata=None):
        """
        Stores or updates table knowledge in the vector database.
        Includes technical schema, high-level description, and column-level meanings.
        """
        col_text = ""
        if column_metadata:
            # Format column meanings for the LLM context 
            col_text = "\nCOLUMN MEANINGS:\n" + "\n".join([f"- {k}: {v}" for k, v in column_metadata.items()])

        full_context = (
            f"TABLE: {table_name}\n"
            f"TECHNICAL SCHEMA: {raw_schema}\n"
            f"BUSINESS DESCRIPTION: {description}"
            f"{col_text}"
        )
        
        # Use upsert to prevent duplicates and allow updates
        self.collection.upsert(
            ids=[table_name],
            documents=[full_context],
            metadatas=[{"table": table_name}]
        )

    def get_context(self, query):
        """Retrieves the most relevant table info for a natural language query."""
        results = self.collection.query(query_texts=[query], n_results=2)
        if results['documents']:
            return "\n\n---\n\n".join(results['documents'][0])
        return ""

    def get_known_tables(self):
        """Returns a list of tables already indexed in memory."""
        data = self.collection.get()
        return data['ids']

    def reset_memory(self):
        """Wipes the vector collection and recreates it."""
        try:
            self.client.delete_collection("business_context")
            self.collection = self.client.get_or_create_collection(
                name="business_context", 
                embedding_function=self.emb_fn
            )
            return True
        except Exception as e:
            print(f"Error resetting memory: {e}")
            return False