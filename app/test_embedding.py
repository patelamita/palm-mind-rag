from embeddings import create_embedding


text = "FastAPI is a Python framework for building APIs."

embedding = create_embedding(text)

print("Embedding created successfully!")
print("Number of values:", len(embedding))
print("First 5 values:", embedding[:5])