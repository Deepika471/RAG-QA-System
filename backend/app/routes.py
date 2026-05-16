import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from pydantic import BaseModel

from app.pdf_loader import load_and_split_pdf

from app.vector_store import create_vector_store

from app.rag_engine import ask_question

from app.memory import (
    clear_memory,
    create_pdf_session,
    create_new_chat,
    get_all_history
)

router = APIRouter()

UPLOAD_DIR = "./uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# Request Model
# ─────────────────────────────────────────────────────────────

class QuestionRequest(BaseModel):

    question: str

    pdf_name: str

    chat_id: str

# ─────────────────────────────────────────────────────────────
# Upload PDF
# ─────────────────────────────────────────────────────────────

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if not file.filename.endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted."
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    # save uploaded file
    with open(file_path, "wb") as f:

        shutil.copyfileobj(
            file.file,
            f
        )

    # load + split
    chunks = load_and_split_pdf(
        file_path
    )

    # create vector db
    create_vector_store(
        chunks
    )

    # create PDF session
    create_pdf_session(
        file.filename
    )

    return {
        "message":
            f"'{file.filename}' uploaded and indexed successfully.",

        "chunks":
            len(chunks)
    }

# ─────────────────────────────────────────────────────────────
# Ask Question
# ─────────────────────────────────────────────────────────────

@router.post("/ask")
async def ask(
    req: QuestionRequest
):

    if not req.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    answer = ask_question(
        query=req.question,
        pdf_name=req.pdf_name,
        chat_id=req.chat_id
    )

    return {
        "answer": answer
    }

# ─────────────────────────────────────────────────────────────
# Create New Chat
# ─────────────────────────────────────────────────────────────

@router.post("/new-chat/{pdf_name}")
async def new_chat(
    pdf_name: str
):

    chat_id = create_new_chat(
        pdf_name
    )

    return {
        "chat_id": chat_id
    }

# ─────────────────────────────────────────────────────────────
# Get Full History
# ─────────────────────────────────────────────────────────────

@router.get("/history")
async def history():

    return {
        "history": get_all_history()
    }

# ─────────────────────────────────────────────────────────────
# Reset Everything
# ─────────────────────────────────────────────────────────────

@router.post("/reset")
async def reset_all():

    clear_memory()

    return {
        "message":
            "Memory cleared successfully."
    }

# ─────────────────────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────────────────────

@router.get("/health")
async def health():

    return {
        "status": "ok"
    }