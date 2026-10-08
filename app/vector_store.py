from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid


client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "documents"
VECTOR_SIZE = 384


def initialize_collection():

    collections = client.get_collections().collections

    if COLLECTION_NAME not in [c.name for c in collections]:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str,
):

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "filename": filename,
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )


def search_similar_chunks(
    query_embedding: list[float],
    limit: int = 5,
):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
    )

    return results.points