from app.embeddings import create_embedding
from app.vector_store import search_similar_chunks


def retrieve_context(
    query: str,
    limit: int = 5,
) -> list[str]:
    """Retrieve the most relevant document chunks for a user query."""

    query_embedding = create_embedding(query)

    results = search_similar_chunks(
        query_embedding=query_embedding,
        limit=limit,
    )

    context = []

    for result in results:
        text = result.payload.get("text")

        if text:
            context.append(text)

    return context


def build_rag_prompt(
    question: str,
    context: list[str],
    history: list[dict[str, str]] | None = None,
) -> str:
    """Build a simple RAG prompt using context and conversation history."""

    joined_context = "\n\n".join(context)

    conversation = ""

    if history:
        conversation = "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in history
        )

    prompt = f"""
Context:
{joined_context}

Conversation history:
{conversation}

Question:
{question}

Answer the question using the context. Give a short, direct answer.
"""

    return prompt.strip()