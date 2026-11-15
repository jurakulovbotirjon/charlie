
import hashlib
import shutil
from pathlib import Path

from charliesynth.memory.repository import MemoryRepository
from charliesynth.perception.text_loader import (
    load_text_file,
    load_pdf_pages,
    split_into_chunks,
    split_pages_into_chunks,
)


class DocumentIngestor:
    def __init__(self):
        self.repository = MemoryRepository()
        self.originals = Path("data/originals")
        self.originals.mkdir(parents=True, exist_ok=True)

    def ingest(self, source: str | Path):
        source = Path(source)

        if not source.is_file():
            raise FileNotFoundError(source)

        extension = source.suffix.lower()

        if extension == ".pdf":
            pages = load_pdf_pages(source)
            chunks = split_pages_into_chunks(pages)
            file_type = "pdf"

        elif extension == ".txt":
            content = load_text_file(source)

            if not content.strip():
                raise ValueError("Document is empty.")

            chunks = [
                {
                    "content": chunk,
                    "page_number": None,
                }
                for chunk in split_into_chunks(content)
            ]
            file_type = "txt"

        else:
            raise ValueError("Only PDF and TXT files are supported.")

        file_hash = hashlib.sha256(
            source.read_bytes()
        ).hexdigest()

        existing = self.repository.get_document_by_hash(file_hash)

        if existing:
            return {
                "status": "already_ingested",
                "document_id": str(existing["id"]),
                "filename": existing["filename"],
            }

        stored_path = self.originals / f"{file_hash}{extension}"
        shutil.copy2(source, stored_path)

        document_id = self.repository.add_document(
            filename=source.name,
            file_type=file_type,
            file_hash=file_hash,
            storage_path=str(stored_path),
        )

        for index, chunk in enumerate(chunks):
            self.repository.add_chunk(
                document_id=document_id,
                chunk_index=index,
                content=chunk["content"],
                page_number=chunk["page_number"],
            )

        return {
            "status": "ingested",
            "document_id": str(document_id),
            "filename": source.name,
            "pages_extracted": len(pages) if extension == ".pdf" else None,
            "chunks_saved": len(chunks),
        }
