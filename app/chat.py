from app.memory import get_chat_history, save_chat_message
from app.rag import retrieve_context, build_rag_prompt


def prepare_chat(
    session_id: str,
    question: str,
) -> str:
    """
    Prepare the RAG prompt for a chat request.
    """

    history = get_chat_history(session_id)

    context = retrieve_context(question)

    prompt = build_rag_prompt(
        question=question,
        context=context,
        history=history,
    )

    save_chat_message(
        session_id=session_id,
        role="user",
        content=question,
    )

    return prompt