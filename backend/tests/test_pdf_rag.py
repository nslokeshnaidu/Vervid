from services.document_ingestion import DocumentIngestionService
from services.vector_db import VectorDBService


# -------------------------
# 1. Ingest PDF
# -------------------------

ingestion = DocumentIngestionService()

pdf_path = "data/documents/DietaryGuidelinesforNINwebsite.pdf"

count = ingestion.ingest_pdf(pdf_path)

print(f"\nStored {count} chunks from PDF.")


# -------------------------
# 2. Search Local RAG
# -------------------------

vector_db = VectorDBService()

query = "Why do we need nutritionally adequate food"

results = vector_db.search(
    query=query,
    top_k=5
)


# -------------------------
# 3. Display evidence
# -------------------------

print("\nQuery:")
print(query)

print("\nRetrieved Evidence:")

for i, result in enumerate(results, start=1):

    print(f"\n--- Result {i} ---")
    print("Source:", result["source"])
    print("Distance:", result["distance"])
    print("Text:")
    print(result["text"])