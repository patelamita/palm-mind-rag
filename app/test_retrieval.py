from app.embeddings import create_embedding
from app.vector_store import search_similar_chunks


query = "What does Palm Mind use for answering questions?"

query_embedding = create_embedding(query)

results = search_similar_chunks(
    query_embedding=query_embedding,
    limit=3,
)

for result in results:
    print("\n--- RESULT ---")
    print("Score:", result.score)
    print("Filename:", result.payload["filename"])
    print("Text:", result.payload["text"])