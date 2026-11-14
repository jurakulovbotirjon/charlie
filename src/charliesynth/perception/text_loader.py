
from pathlib import Path


def load_text_file(path: str | Path) -> str:
    """Read a UTF-8 text document."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    if file_path.suffix.lower() != ".txt":
        raise ValueError("Only .txt files are supported currently.")

    return file_path.read_text(encoding="utf-8")


def split_into_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:
    """Split text into overlapping chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size.")

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks
