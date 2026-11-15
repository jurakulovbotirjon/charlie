
from uuid import UUID

from charliesynth.memory.database import get_connection


class MemoryRepository:

    
    def search_chunks(self, question: str, limit: int = 5) -> list[dict]:
        """Retrieve relevant passages using PostgreSQL full-text search."""

        if not question.strip():
            return []

        query = """
            SELECT
                kc.id,
                d.filename,
                kc.content,
                kc.page_number,
                ts_rank(
                    to_tsvector('english', kc.content),
                    plainto_tsquery('english', %s)
                ) AS relevance
            FROM knowledge_chunks kc
            JOIN documents d ON d.id = kc.document_id
            WHERE to_tsvector('english', kc.content)
                  @@ plainto_tsquery('english', %s)
            ORDER BY relevance DESC
            LIMIT %s;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (question, question, limit))
                rows = cursor.fetchall()

        return [
            {
                "chunk_id": row[0],
                "filename": row[1],
                "content": row[2],
                "page_number": row[3],
                "relevance": float(row[4]),
            }
            for row in rows
        ]
    
    def get_document_by_hash(self, file_hash: str):
        """Find an already registered document by SHA-256 hash."""

        query = """
            SELECT id, filename, storage_path
            FROM documents
            WHERE file_hash = %s;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (file_hash,))
                row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "filename": row[1],
            "storage_path": row[2],
        }

    def add_document(
        self,
        filename: str,
        file_type: str,
        file_hash: str,
        storage_path: str,
    ) -> UUID:
        """Register a document in permanent memory."""

        query = """
            INSERT INTO documents (
                filename,
                file_type,
                file_hash,
                storage_path
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (filename, file_type, file_hash, storage_path),
                )
                document_id = cursor.fetchone()[0]

        return document_id

    def add_chunk(
        self,
        document_id: UUID,
        chunk_index: int,
        content: str,
        page_number: int | None = None,
    ) -> int:
        """Store an extracted text chunk."""

        query = """
            INSERT INTO knowledge_chunks (
                document_id,
                chunk_index,
                content,
                page_number
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (document_id, chunk_index, content, page_number),
                )
                chunk_id = cursor.fetchone()[0]

        return chunk_id

    def get_document_chunks(self, document_id: UUID) -> list[dict]:
        """Retrieve all chunks belonging to a document."""

        query = """
            SELECT id, chunk_index, content, page_number
            FROM knowledge_chunks
            WHERE document_id = %s
            ORDER BY chunk_index;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (document_id,))
                rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "chunk_index": row[1],
                "content": row[2],
                "page_number": row[3],
            }
            for row in rows
        ]

    def list_documents(self) -> list[dict]:
        """List registered documents."""

        query = """
            SELECT id, filename, file_type, processing_status, created_at
            FROM documents
            ORDER BY created_at DESC;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "filename": row[1],
                "file_type": row[2],
                "status": row[3],
                "created_at": row[4],
            }
            for row in rows
        ]
