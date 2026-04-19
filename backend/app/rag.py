from dataclasses import dataclass
from typing import List, Dict, Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    doc_id: str
    chunk_id: int
    text: str


class InMemoryLegalRAG:
    def __init__(self) -> None:
        self._chunks: List[Chunk] = []
        self._vectorizer = TfidfVectorizer(stop_words="english")
        self._matrix = None

    def ingest(self, doc_id: str, text: str, chunk_size: int = 700) -> int:
        slices = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
        start_idx = len(self._chunks)
        for i, chunk_text in enumerate(slices):
            self._chunks.append(Chunk(doc_id=doc_id, chunk_id=start_idx + i, text=chunk_text))
        self._reindex()
        return len(slices)

    def _reindex(self) -> None:
        corpus = [c.text for c in self._chunks]
        if not corpus:
            self._matrix = None
            return
        self._matrix = self._vectorizer.fit_transform(corpus)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if self._matrix is None or not self._chunks:
            return []
        query_vec = self._vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self._matrix)[0]
        top_idx = np.argsort(sims)[::-1][:top_k]

        results: List[Dict[str, Any]] = []
        for idx in top_idx:
            c = self._chunks[int(idx)]
            results.append(
                {
                    "doc_id": c.doc_id,
                    "chunk_id": c.chunk_id,
                    "score": float(sims[int(idx)]),
                    "text": c.text,
                }
            )
        return results
