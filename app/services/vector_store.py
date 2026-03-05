from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = None
documents = []
index = None


def get_model():

    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def add_document(text: str, metadata: dict):

    global index

    model = get_model()

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    embeddings = model.encode(chunks)

    if index is None:

        dim = embeddings.shape[1]

        index = faiss.IndexFlatL2(dim)

    index.add(np.array(embeddings))

    for chunk in chunks:

        documents.append({
            "text": chunk,
            "metadata": metadata
        })


def search(query: str, top_k: int = 5):

    if index is None:
        return []

    model = get_model()

    query_vector = model.encode([query])

    distances, ids = index.search(np.array(query_vector), top_k)

    results = []

    for i in ids[0]:

        if i < len(documents):

            results.append(documents[i])

    return results