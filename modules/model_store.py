from functools import lru_cache

import spacy
from sentence_transformers import SentenceTransformer

from modules.config import MODEL_NAME


@lru_cache(maxsize=1)
def get_nlp():
    return spacy.load("en_core_web_sm")


@lru_cache(maxsize=1)
def get_embedding_model():
    try:
        return SentenceTransformer(MODEL_NAME, local_files_only=True)
    except Exception:
        return SentenceTransformer(MODEL_NAME)
