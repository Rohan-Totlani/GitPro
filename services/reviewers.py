from typing import List, Tuple
import numpy as np
import faiss

from .embeddings import embed_texts


class ReviewerEngine:
    """Simple in-memory reviewer suggestion engine using embeddings and FAISS."""
    def __init__(self, dim: int = 768):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add_documents(self, docs: List[Tuple[str, dict]]):
        # docs: list of (text, metadata)
        texts = [d[0] for d in docs]
        embs = embed_texts(texts)
        if embs.ndim == 1:
            embs = np.expand_dims(embs, 0)
        self.index.add(embs.astype('float32'))
        self.metadata.extend([d[1] for d in docs])

    def suggest(self, query: str, k: int = 5) -> List[dict]:
        q_emb = embed_texts([query]).astype('float32')
        D, I = self.index.search(q_emb, k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results
