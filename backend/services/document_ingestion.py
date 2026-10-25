from pypdf import PdfReader
from services.vector_db import VectorDBService


class DocumentIngestionService:
    """
    Handles document processing and ingestion
    into VeriVid's local RAG database.
    """

    def __init__(self):
        self.vector_db = VectorDBService()

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 150,
        overlap: int = 30
    ):
        """
        Split text into word-based overlapping chunks.
        Prevents words from being cut in half.
        """

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk_words = words[start:end]

            chunk = " ".join(chunk_words)

            if chunk:
                chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    def ingest_text(self, text: str, source: str):
        """
        Chunk text and store it in the vector database.
        """

        chunks = self.chunk_text(text)

        documents = []

        for index, chunk in enumerate(chunks):

            documents.append({
                "id": f"{source}_{index}",
                "text": chunk,
                "source": source
            })

        self.vector_db.add_documents(documents)

        return len(documents)

    def ingest_pdf(self, file_path: str):
        """
        Extract text from a PDF and store it
        in VeriVid's Local RAG.
        """

        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        full_text = "\n".join(pages)

        return self.ingest_text(
            text=full_text,
            source=file_path
        )