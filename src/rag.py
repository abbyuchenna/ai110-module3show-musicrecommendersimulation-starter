"""
rag (retrieval-augmented generation) module for the music recommender system.

loads a plain-text knowledge base, indexes it with tf-idf, and retrieves
the most relevant chunks for a given user query. retrieved chunks are injected
into the gemma prompt to improve genre/mood/energy parsing accuracy.
"""

import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_KB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "music_knowledge.txt")


def load_knowledge_base(path: str = _KB_PATH) -> list:
    """load and split the knowledge base into individual chunks by blank line."""
    with open(path, "r") as f:
        text = f.read()
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    return chunks


def retrieve(query: str, chunks: list, top_k: int = 3) -> list:
    """
    retrieve the top_k most relevant knowledge chunks for a given query.
    uses tf-idf vectorization and cosine similarity.
    returns a list of matching text chunks (strings).
    """
    if not chunks:
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    all_texts = chunks + [query]
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    query_vec = tfidf_matrix[-1]
    doc_vecs = tfidf_matrix[:-1]

    similarities = cosine_similarity(query_vec, doc_vecs)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]

    # only return chunks with non-zero similarity
    return [chunks[i] for i in top_indices if similarities[i] > 0]


# load once at import time so it isn't re-read on every call
_chunks = load_knowledge_base()


def get_context(query: str, top_k: int = 3) -> str:
    """
    retrieve relevant knowledge and return it as a formatted string
    ready to be injected into a prompt.
    """
    results = retrieve(query, _chunks, top_k=top_k)
    if not results:
        return ""
    return "\n\n".join(results)
