import json

import redis


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


def get_chat_history(
    session_id: str,
) -> list[dict[str, str]]:
    """Retrieve conversation history for a session."""

    history = redis_client.get(f"chat:{session_id}")

    if not history:
        return []

    return json.loads(history)


def save_chat_message(
    session_id: str,
    role: str,
    content: str,
) -> None:
    """Save a chat message to Redis."""

    history = get_chat_history(session_id)

    history.append(
        {
            "role": role,
            "content": content,
        }
    )

    redis_client.set(
        f"chat:{session_id}",
        json.dumps(history),
    )