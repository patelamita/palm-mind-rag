from ollama import chat


MODEL_NAME = "qwen2.5:0.5b"


def generate_response(prompt: str) -> str:
    """Generate a response using the local Ollama model."""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]