from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "System Design is used to build scalable applications",
    "Python is a programming language",
    "Machine Learning uses data for predictions"
]

embeddings = model.encode(documents)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings, dtype=np.float32))

query = "How do we build scalable systems?"

query_embedding = model.encode([query])

D, I = index.search(
    np.array(query_embedding, dtype=np.float32),
    k=1
)

print("Best Match:")
print(documents[I[0][0]])
