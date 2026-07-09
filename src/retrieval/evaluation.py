from dataclasses import dataclass

from src.retrieval.models import HybridSearchResult


@dataclass(frozen=True)
class RetrievalTestCase:
    """Represents one retrieval evaluation question."""

    question: str
    expected_chunk_ids: list[str]


@dataclass(frozen=True)
class RetrievalEvaluationResult:
    """ Represents evaluation result for one question."""

    question: str
    expected_chunk_ids: list[str]
    returned_chunk_ids: list[str]
    is_success: bool


def evaluate_retrieval_result(
    question: str,
    expected_chunk_ids: list[str],
    search_results: list[HybridSearchResult],
) -> RetrievalEvaluationResult:
    """ Checks if at least one expected chunk is present in search results."""

    returned_chunk_ids = [
        result.record.chunk_id
        for result in search_results
    ]

    is_success = any(
        expected_chunk_id in returned_chunk_ids
        for expected_chunk_id in expected_chunk_ids
    )

    return RetrievalEvaluationResult(
        question=question,
        expected_chunk_ids=expected_chunk_ids,
        returned_chunk_ids=returned_chunk_ids,
        is_success=is_success,
    )