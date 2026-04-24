"""
Retrieval-Augmented Generation (RAG) module for legal documents.

This module implements an in-memory RAG system using TF-IDF vectorization
and cosine similarity for legal document retrieval.
"""

from dataclasses import dataclass
from typing import List, Dict, Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    """Represents a chunk of a legal document."""
    doc_id: str
    chunk_id: int
    text: str


class InMemoryLegalRAG:
    """
    In-memory Retrieval-Augmented Generation system for legal documents.
    
    Uses TF-IDF vectorization to index and retrieve relevant legal text chunks
    based on semantic similarity to user queries.
    """

    def __init__(self, chunk_size: int = 700) -> None:
        """
        Initialize the RAG system.
        
        Args:
            chunk_size: Size of text chunks in characters (default: 700)
        """
        self._chunks: List[Chunk] = []
        self._vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            lowercase=True,
            strip_accents="unicode",
        )
        self._matrix = None
        self.chunk_size = chunk_size

    def ingest(self, doc_id: str, text: str, chunk_size: int | None = None) -> int:
        """
        Ingest a legal document and split it into chunks.
        
        Args:
            doc_id: Unique document identifier
            text: Full text of the document
            chunk_size: Override default chunk size (optional)
        
        Returns:
            Number of chunks created
        """
        size = chunk_size or self.chunk_size
        
        # Split text into chunks
        slices = [text[i : i + size] for i in range(0, len(text), size)]
        
        # Create Chunk objects and add to store
        start_idx = len(self._chunks)
        for i, chunk_text in enumerate(slices):
            if chunk_text.strip():  # Skip empty chunks
                self._chunks.append(
                    Chunk(doc_id=doc_id, chunk_id=start_idx + i, text=chunk_text)
                )
        
        # Rebuild index
        self._reindex()
        return len(slices)

    def _reindex(self) -> None:
        """Rebuild the TF-IDF index from current chunks."""
        corpus = [c.text for c in self._chunks]
        if not corpus:
            self._matrix = None
            return
        self._matrix = self._vectorizer.fit_transform(corpus)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant document chunks for a query.
        
        Args:
            query: User's search query
            top_k: Number of top results to return (default: 3)
        
        Returns:
            List of relevant chunks with scores, sorted by relevance
        """
        if self._matrix is None or not self._chunks:
            return []
        
        # Vectorize query
        query_vec = self._vectorizer.transform([query])
        
        # Compute similarity scores
        sims = cosine_similarity(query_vec, self._matrix)[0]
        
        # Get indices of top-k results
        top_idx = np.argsort(sims)[::-1][:top_k]

        # Build results
        results: List[Dict[str, Any]] = []
        for idx in top_idx:
            c = self._chunks[int(idx)]
            score = float(sims[int(idx)])
            
            # Only include results with non-zero relevance
            if score > 0:
                results.append(
                    {
                        "doc_id": c.doc_id,
                        "chunk_id": c.chunk_id,
                        "score": score,
                        "text": c.text,
                    }
                )
        
        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the indexed documents."""
        return {
            "total_chunks": len(self._chunks),
            "is_indexed": self._matrix is not None,
            "unique_docs": len(set(c.doc_id for c in self._chunks)),
        }

