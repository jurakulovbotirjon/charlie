
import hashlib
import shutil
from pathlib import Path

from charliesynth.memory.repository import MemoryRepository
from charliesynth.perception.text_loader import (
    load_text_file,
    split_into_chunks,
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

        content = load_text_file(source)

        if not content.strip():
            raise ValueError("Document is empty.")

        file_hash = hashlib.sha256(source.read_bytes()).hexdigest()

        # Avoid registering the same file twice.
        for document in self.repository.list_documents():
            if document["id"] and document["filename"] == source.name:
                pass

        stored_path = self.originals / f"{file_hash}.txt"

        if not stored_path.exists():
            shutil.copy2(source, stored_path)

        document_id = self.repository.add_document(
            filename=source.name,
            file_type="txt",
            file_hash=file_hash,
            storage_path=str(stored_path),
        )

        chunks = split_into_chunks(content)

        for index, chunk in enumerate(chunks):
            self.repository.add_chunk(
                document_id=document_id,
                chunk_index=index,
                content=chunk,
            )

        return {
            "document_id": str(document_id),
            "filename": source.name,
            "chunks_saved": len(chunks),
            "storage_path": str(stored_path),
        }
