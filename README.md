\# Palm Mind AI - RAG Backend



A FastAPI-based backend implementing document ingestion, vector search, conversational RAG, Redis chat memory, and LLM-powered interview booking.



\## Features



\- PDF and TXT document upload

\- Two selectable chunking strategies:

&#x20; - Fixed-size chunking

&#x20; - Paragraph-based chunking

\- Local text embeddings using Sentence Transformers

\- Qdrant vector database for similarity search

\- SQLite for document metadata and interview bookings

\- Redis for conversational chat memory

\- Custom RAG pipeline without RetrievalQAChain

\- Local LLM using Ollama

\- LLM-based interview detail extraction

\- Interview booking through the conversational API



\## Architecture



```text

Document

&#x20;  ↓

Text Extraction

&#x20;  ↓

Chunking

&#x20;  ↓

Embeddings

&#x20;  ↓

Qdrant Vector Database





User Query

&#x20;  ↓

Query Embedding

&#x20;  ↓

Qdrant Similarity Search

&#x20;  ↓

Retrieved Context + Chat History

&#x20;  ↓

LLM

&#x20;  ↓

Response





Interview Request

&#x20;  ↓

LLM Detail Extraction

&#x20;  ↓

SQLite Booking

```



\## Tech Stack



\- Python

\- FastAPI

\- Qdrant

\- Redis

\- SQLite

\- SQLAlchemy

\- Sentence Transformers

\- Ollama

\- Qwen 2.5 0.5B



\## Setup



\### 1. Create and activate a virtual environment



```bash

python -m venv venv

venv\\Scripts\\activate

```



\### 2. Install dependencies



```bash

pip install -r requirements.txt

```



\### 3. Start Qdrant and Redis



```bash

docker compose up -d

```



\### 4. Make sure Ollama is installed and the model is available



```bash

ollama pull qwen2.5:0.5b

```



\### 5. Initialize the database



```bash

python -m app.init\_db

```



\### 6. Start the API



```bash

uvicorn app.main:app --reload

```



The API will be available at:



```text

http://127.0.0.1:8000

```



Interactive API documentation:



```text

http://127.0.0.1:8000/docs

```



\## API Endpoints



\### `POST /documents`



Upload a PDF or TXT document and select a chunking strategy.



Supported strategies:



\- `fixed`

\- `paragraph`



The document is parsed, chunked, embedded, and stored in Qdrant. Document metadata is stored in SQLite.



\### `POST /chat`



Send a question using a session ID.



The endpoint:



\- retrieves relevant document chunks

\- uses Redis to maintain conversation history

\- builds a custom RAG prompt

\- generates an answer using the local LLM

\- supports interview booking requests



Example:



```json

{

&#x20; "session\_id": "test-session",

&#x20; "question": "What is FastAPI?"

}

```



\### `POST /book-interview`



Extract interview details using the LLM and store the booking in SQLite.



Example:



```json

{

&#x20; "session\_id": "booking-session",

&#x20; "question": "I want to book an interview. My name is Amita Kumari, my email is amita@example.com, on October 20, 2026 at 2:00 PM."

}

```



\## Storage



\- \*\*Qdrant:\*\* document chunks and embeddings

\- \*\*SQLite:\*\* document metadata and interview bookings

\- \*\*Redis:\*\* conversational chat history



\## Notes



The project uses a lightweight local language model through Ollama so that the backend can run without requiring an external LLM API.

