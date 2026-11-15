
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from uuid import uuid4

from charliesynth.core.brain import CharlieSynth
from charliesynth.memory.repository import MemoryRepository
from charliesynth.perception.ingestor import DocumentIngestor


app = FastAPI(
    title="CharlieSynth API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

brain = CharlieSynth()
repository = MemoryRepository()

UPLOAD_DIR = Path("data/inbox")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class Question(BaseModel):
    question: str


@app.get("/api/status")
def status():
    return brain.status()


@app.get("/api/documents")
def documents():
    return repository.list_documents()


@app.post("/api/ask")
def ask(data: Question):
    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    return {
        "answer": brain.answer(data.question)
    }


@app.post("/api/search")
def search(data: Question):
    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    return {
        "results": repository.search_chunks(data.question)
    }


@app.post("/api/ingest")
async def ingest(file: UploadFile = File(...)):
    filename = Path(file.filename or "upload").name
    suffix = Path(filename).suffix.lower()

    if suffix not in {".pdf", ".txt"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    temp_path = UPLOAD_DIR / f"{uuid4().hex}{suffix}"

    try:
        with temp_path.open("wb") as destination:
            while chunk := await file.read(1024 * 1024):
                destination.write(chunk)

        result = DocumentIngestor().ingest(temp_path)

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    finally:
        temp_path.unlink(missing_ok=True)
        await file.close()
