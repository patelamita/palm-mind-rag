from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel

from app.llm import generate_response
from app.chat import prepare_chat
from app.booking_extractor import extract_booking_details
from app.booking import create_booking
from app.memory import save_chat_message
from app.document_parser import (
    extract_text_from_txt,
    extract_text_from_pdf,
)

from app.chunking import (
    fixed_size_chunks,
    paragraph_chunks,
)

from app.embeddings import create_embedding

from app.vector_store import (
    initialize_collection,
    store_chunks,
    search_similar_chunks,
)

from app.database import SessionLocal
from app.models import Document


app = FastAPI()


# Initialize Qdrant collection when the application starts
initialize_collection()


@app.get("/")
def home():
    return {
        "message": "Palm Mind RAG Backend is running!"
    }


@app.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: str = Form("fixed"),
):
    allowed_extensions = [".pdf", ".txt"]

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided",
        )

    file_extension = "." + file.filename.split(".")[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed",
        )

    content = await file.read()

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(content)

    # Extract text
    if file_extension == ".pdf":
        text = extract_text_from_pdf(content)
    else:
        text = extract_text_from_txt(content)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from the document",
        )

    # Select chunking strategy
    if chunking_strategy == "fixed":
        chunks = fixed_size_chunks(text)

    elif chunking_strategy == "paragraph":
        chunks = paragraph_chunks(text)

    else:
        raise HTTPException(
            status_code=400,
            detail="chunking_strategy must be 'fixed' or 'paragraph'",
        )

    # Generate embeddings
    embeddings = [
        create_embedding(chunk)
        for chunk in chunks
    ]

    # Store chunks and embeddings in Qdrant
    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename,
    )

    # Save document metadata in SQLite
    db = SessionLocal()

    try:
        document = Document(
            filename=file.filename,
            file_type=file_extension,
            chunking_strategy=chunking_strategy,
            number_of_chunks=len(chunks),
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        document_id = document.id

    finally:
        db.close()

    return {
        "document_id": document_id,
        "filename": file.filename,
        "message": "Document processed successfully",
        "text_length": len(text),
        "chunking_strategy": chunking_strategy,
        "chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
    }


class ChatRequest(BaseModel):
    session_id: str
    question: str


@app.post("/chat")
def chat(request: ChatRequest):

    # Check for interview-booking intent first
    booking_keywords = [
        "book an interview",
        "book interview",
        "schedule an interview",
        "schedule interview",
        "interview booking",
    ]

    is_booking_request = any(
        keyword in request.question.lower()
        for keyword in booking_keywords
    )

    if is_booking_request:

        booking_details = extract_booking_details(request.question)

        if all(booking_details.values()):

            db = SessionLocal()

            try:
                booking = create_booking(
                    db=db,
                    name=booking_details["name"],
                    email=booking_details["email"],
                    interview_date=booking_details["interview_date"],
                    interview_time=booking_details["interview_time"],
                )

                answer = (
                    f"Your interview has been booked successfully for "
                    f"{booking.interview_date} at {booking.interview_time}."
                )

                save_chat_message(
                    session_id=request.session_id,
                    role="user",
                    content=request.question,
                )

                save_chat_message(
                    session_id=request.session_id,
                    role="assistant",
                    content=answer,
                )

                return {
                    "session_id": request.session_id,
                    "question": request.question,
                    "answer": answer,
                    "booking_id": booking.id,
                }

            finally:
                db.close()

        else:
            return {
                "session_id": request.session_id,
                "question": request.question,
                "answer": (
                    "Please provide your name, email, "
                    "interview date, and interview time."
                ),
            }

    # Normal RAG conversation
    prompt = prepare_chat(
        session_id=request.session_id,
        question=request.question,
    )

    answer = generate_response(prompt)

    save_chat_message(
        session_id=request.session_id,
        role="assistant",
        content=answer,
    )

    return {
        "session_id": request.session_id,
        "question": request.question,
        "answer": answer,
    }