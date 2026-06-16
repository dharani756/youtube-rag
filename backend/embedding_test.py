from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

texts = [
    "System Design",
    "Machine Learning",
    "Artificial Intelligence"
]

embeddings = model.encode(texts)

print(embeddings.shape)