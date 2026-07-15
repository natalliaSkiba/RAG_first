import unittest

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.provider import EmbeddingProvider
from src.retrieval.models import RetrievalRecord
from src.retrieval.service import RetrievalService


class FakeEmbeddingProvider(EmbeddingProvider):
    """ Provides a fixed query embedding without loading a real model."""

    def __init__(self) -> None:
        super().__init__(
            config=DEFAULT_EMBEDDING_CONFIG,
        )

        self.call_count = 0
        self.received_texts: list[str] = []

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """ Return one fixed vector for every received text. """

        self.call_count += 1
        self.received_texts.extend(texts)

        vector = [
            0.0
            for _ in range(self.config.dimension)
        ]
        vector[0] = 1.0

        return [
            vector.copy()
            for _ in texts
        ]


class RetrievalServiceTest(unittest.TestCase):
    """ Tests retrieval service. """

    def test_should_return_most_relevant_record(self) -> None:
        """Return the record closest to the query embedding. """

        provider = FakeEmbeddingProvider()
        dimension = provider.config.dimension

        relevant_embedding = [
            0.0
            for _ in range(dimension)
        ]
        relevant_embedding[0] = 1.0

        unrelated_embedding = [
            0.0
            for _ in range(dimension)
        ]
        unrelated_embedding[1] = 1.0

        relevant_record = RetrievalRecord(
            chunk_id="chunk_relevant",
            text="Premier contenu.",
            embedding=relevant_embedding,
            metadata={"heading": "Première section"},
            embedding_metadata={},
        )

        unrelated_record = RetrievalRecord(
            chunk_id="chunk_unrelated",
            text="Deuxième contenu.",
            embedding=unrelated_embedding,
            metadata={"heading": "Deuxième section"},
            embedding_metadata={},
        )

        service = RetrievalService(
            provider=provider,
            records=[
                unrelated_record,
                relevant_record,
            ],
        )

        question = "Quelle information est correcte ?"

        results = service.search(
            question=question,
            top_k=1,
        )

        self.assertEqual(1, len(results))
        self.assertEqual(
            "chunk_relevant",
            results[0].record.chunk_id,
        )
        self.assertEqual(1, provider.call_count)
        self.assertEqual(
            [
                f"{provider.config.query_prefix}{question}"
            ],
            provider.received_texts,
        )