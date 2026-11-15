
from pathlib import Path
from pypdf import PdfReader


def load_text_file(path: str | Path) -> str:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    if file_path.suffix.lower() != ".txt":
        raise ValueError("Only .txt files are supported.")

    return file_path.read_text(encoding="utf-8").replace("\x00", "")


def load_pdf_pages(path: str | Path) -> list[dict]:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Only .pdf files are supported.")

    reader = PdfReader(str(file_path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        content = page.extract_text() or ""
        content = content.replace("\x00", "")

        if content.strip():
            pages.append({
                "page_number": page_number,
                "content": content.strip(),
            })

    if not pages:
        raise ValueError("No extractable text found in this PDF.")

    return pages


def split_into_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid overlap.")

    text = text.replace("\x00", "").strip()

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


def split_pages_into_chunks(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    chunks = []

    for page in pages:
        page_chunks = split_into_chunks(
            page["content"],
            chunk_size,
            overlap,
        )

        for chunk in page_chunks:
            chunks.append({
                "content": chunk,
                "page_number": page["page_number"],
            })

    return chunks
