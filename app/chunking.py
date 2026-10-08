def fixed_size_chunks(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - overlap

    return chunks
def paragraph_chunks(
    text: str,
    max_chunk_size: int = 500,
) -> list[str]:

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        if len(current_chunk) + len(paragraph) <= max_chunk_size:
            current_chunk += paragraph + "\n\n"

        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            current_chunk = paragraph + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks