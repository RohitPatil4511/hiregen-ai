import numpy as np
from backend.rag.embeddings import get_embedding
from backend.rag.vectorstore import load_vectorstore

def retrieve_similar(query: str, top_k: int = 3):
    index, metadata = load_vectorstore()
    if index is None:
        return []
    query_vec = get_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_vec, top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            results.append({
                "score": float(distances[0][i]),
                "data": metadata[idx]
            })
    return results