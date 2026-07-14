import unittest

from src.quiz.context import build_quiz_context
from src.retrieval.models import (
    HybridSearchResult,
    RetrievalRecord,
)


class BuildQuizContextTest(unittest.TestCase):
    """Tests quiz context creation."""

    def test_should_build_context_from_search_result(self) -> None:
        record = RetrievalRecord(
            chunk_id="chunk_001",
            text="L'agent doit protéger la circulation.",
            embedding=[],
            metadata={"heading": "Détresse"},
            embedding_metadata={},
        )

        result = HybridSearchResult(
            rank=1,
            score=0.9,
            semantic_score=0.8,
            keyword_score=0.1,
            record=record,
        )

        context = build_quiz_context([result])

        self.assertIn("CHUNK_ID: chunk_001", context)
        self.assertIn("HEADING: Détresse", context)
        self.assertIn(
            "L'agent doit protéger la circulation.",
            context,
        )

    def test_should_reject_empty_results(self) -> None:
        with self.assertRaises(ValueError):
            build_quiz_context([])