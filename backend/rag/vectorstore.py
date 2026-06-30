import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "data/faiss_index.bin"
META_PATH = "data/faiss_meta.pkl"

def save_to_vectorstore(embeddings, metadata: list):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)
    print(f"Saved {len(metadata)} entries to vector store.")

def load_vectorstore():
    if not os.path.exists(INDEX_PATH):
        return None, []
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata