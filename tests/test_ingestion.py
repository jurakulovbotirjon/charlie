
from pathlib import Path

from charliesynth.perception.text_loader import (
    load_text_file,
    split_into_chunks,
)


def test_load_text_file():
    path = Path("data/inbox/first_book.txt")
    content = load_text_file(path)

    assert "Knowledge is built" in content


def test_split_into_chunks():
    text = "A" * 2500

    chunks = split_into_chunks(
        text,
        chunk_size=1000,
        overlap=150,
    )

    assert len(chunks) == 3
    assert chunks[0][-150:] == chunks[1][:150]

