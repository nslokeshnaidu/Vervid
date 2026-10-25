import chromadb
from sentence_transformers import SentenceTransformer


class VectorDBService:
    """
    Handles VeriVid's local RAG vector database.
    """

    def __init__(self):
        # Load embedding model
        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # Persistent ChromaDB database
        self.client = chromadb.PersistentClient(
            path="./data/chroma_db"
        )

        # Create the collection if it doesn't exist
        self.collection = self.client.get_or_create_collection(
            name="verivid_knowledge"
        )

    def add_documents(self, documents):
        """
        Add evidence documents/chunks to the local knowledge base.

        Expected format:

        [
            {
                "id": "doc_1",
                "text": "...",
                "source": "WHO"
            }
        ]
        """

        if not documents:
            return

        texts = [document["text"] for document in documents]

        ids = [document["id"] for document in documents]

        metadatas = [
            {
                "source": document.get("source", "Unknown")
            }
            for document in documents
        ]

        embeddings = self.embedding_model.encode(
            texts
        ).tolist()

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query: str, top_k: int = 5):
        """
        Retrieve evidence relevant to a claim.
        """

        # Don't query an empty database
        if self.collection.count() == 0:
            return []

        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count())
        )

        evidence = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):
            evidence.append({
                "text": document,
                "source": metadata.get("source", "Unknown"),
                "source_type": "local",
                "distance": distance
            })

        return evidence