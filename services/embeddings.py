import os
from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL_NAME = os.environ.get("EMBEDDING_MODEL", "all-mpnet-base-v2")
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed_texts(texts):
    model = get_model()
    emb = model.encode(texts, convert_to_numpy=True)
    return emb
