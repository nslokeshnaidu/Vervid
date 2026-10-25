from services.document_ingestion import DocumentIngestionService
from services.vector_db import VectorDBService


ingestion = DocumentIngestionService()

sample_text = """
India is a country in South Asia.

India consists of 28 states and 8 union territories.

New Delhi is the capital of India.

The Constitution of India defines India as a union of states.
"""

count = ingestion.ingest_text(
    text=sample_text,
    source="test_india_document"
)

print(f"Stored {count} chunks.")


vector_db = VectorDBService()

results = vector_db.search(
    query="How many states does India have?",
    top_k=3
)

print("\nRetrieved Evidence:")

for result in results:
    print("\n----------------")
    print("Source:", result["source"])
    print("Text:", result["text"])
    print("Distance:", result["distance"])