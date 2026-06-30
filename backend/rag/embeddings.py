from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    return model.encode(text, convert_to_numpy=True)

def get_embeddings(texts: list):
    return model.encode(texts, convert_to_numpy=True)