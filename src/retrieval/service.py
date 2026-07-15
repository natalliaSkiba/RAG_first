from src.embedding.provider import EmbeddingProvider
from src.retrieval.models import (
    HybridSearchResult,
    RetrievalRecord,
)
from src.retrieval.query import generate_query_embedding
from src.retrieval.search import search_by_vector_hybrid


class RetrievalService:
    """Runs hybrid retrieval using a prepared provider and records. """

    def __init__(
        self,
        provider: EmbeddingProvider,
        records: list[RetrievalRecord],
    ) -> None:
        self.provider = provider
        self.records = records

    def search(
        self,
        question: str,
        top_k: int = 5,
    ) -> list[HybridSearchResult]:
        """ Find the most relevant chunks for a user question.  """

        query_embedding = generate_query_embedding(
            question=question,
            provider=self.provider,
        )

        return search_by_vector_hybrid(
            question=question,
            query_embedding=query_embedding,
            records=self.records,
            top_k=top_k,
        )