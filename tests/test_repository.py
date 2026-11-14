
from charliesynth.memory.repository import MemoryRepository


def test_repository_methods_exist():
    repository = MemoryRepository()

    assert callable(repository.add_document)
    assert callable(repository.add_chunk)
    assert callable(repository.get_document_chunks)
    assert callable(repository.list_documents)
