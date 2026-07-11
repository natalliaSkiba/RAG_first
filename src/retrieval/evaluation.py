import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.retrieval.models import HybridSearchResult, SearchResult


@dataclass(frozen=True)
class RetrievalTestCase:
    """Represents one retrieval evaluation question."""

    question: str
    expected_chunk_ids: list[str]
    topic: str
    notes: str


@dataclass(frozen=True)
class RetrievalEvaluationResult:
    """Represents evaluation result for one question."""

    question: str
    expected_chunk_ids: list[str]
    returned_chunk_ids: list[str]
    is_success: bool


def load_retrieval_test_cases(
    file_path: Path,
) -> list[RetrievalTestCase]:
    """Loads retrieval test cases from a JSON file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Retrieval test cases file not found: {file_path}"
        )

    with file_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        raw_data = json.load(file)

    if not isinstance(raw_data, list):
        raise ValueError(
            "Retrieval test cases JSON must contain a list"
        )

    test_cases: list[RetrievalTestCase] = []

    for index, item in enumerate(raw_data, start=1):
        if not isinstance(item, dict):
            raise ValueError(
                f"Test case #{index} must be a JSON object"
            )

        test_cases.append(
            _parse_retrieval_test_case(
                item=item,
                index=index,
            )
        )

    return test_cases


def _parse_retrieval_test_case(
    item: dict[str, Any],
    index: int,
) -> RetrievalTestCase:
    """Parses one retrieval test case from dictionary."""

    required_fields = [
        "question",
        "expected_chunk_ids",
        "topic",
        "notes",
    ]

    for field in required_fields:
        if field not in item:
            raise ValueError(
                f"Missing field '{field}' in test case #{index}"
            )

    question = str(item["question"]).strip()
    topic = str(item["topic"]).strip()
    notes = str(item["notes"]).strip()

    expected_chunk_ids_raw = item["expected_chunk_ids"]

    if not question:
        raise ValueError(
            f"Question must not be empty in test case #{index}"
        )

    if not isinstance(expected_chunk_ids_raw, list):
        raise ValueError(
            f"expected_chunk_ids must be a list in test case #{index}"
        )

    expected_chunk_ids = [
        str(chunk_id).strip()
        for chunk_id in expected_chunk_ids_raw
        if str(chunk_id).strip()
    ]

    if not expected_chunk_ids:
        raise ValueError(
            f"expected_chunk_ids must not be empty in test case #{index}"
        )

    return RetrievalTestCase(
        question=question,
        expected_chunk_ids=expected_chunk_ids,
        topic=topic,
        notes=notes,
    )


def extract_chunk_ids_from_search_results(
    search_results: list[SearchResult] | list[HybridSearchResult],
) -> list[str]:
    """Extracts chunk ids from search results."""

    return [
        result.record.chunk_id
        for result in search_results
    ]


def evaluate_retrieval_result(
    question: str,
    expected_chunk_ids: list[str],
    returned_chunk_ids: list[str],
) -> RetrievalEvaluationResult:
    """Checks if at least one expected chunk is present in returned results."""

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

@dataclass(frozen=True)
class RetrievalMetrics:
    """ Represents ranking metrics for one retrieval result. """

    hit_at_1: float
    hit_at_k: float
    reciprocal_rank_at_k: float
    recall_at_k: float


def calculate_hit_at_1(
    expected_chunk_ids: list[str],
    returned_chunk_ids: list[str],
) -> float:
    """Calculates Hit@1.
    Hit@1 = 1 if the first returned chunk is expected."""

    if not returned_chunk_ids:
        return 0.0

    first_returned_chunk_id = returned_chunk_ids[0]

    if first_returned_chunk_id in expected_chunk_ids:
        return 1.0

    return 0.0


def calculate_hit_at_k(
    expected_chunk_ids: list[str],
    returned_chunk_ids: list[str],
    k: int,
) -> float:
    """ Calculates Hit@K.
    Hit@K = 1 if at least one expected chunk is found in top K."""

    top_k_chunk_ids = returned_chunk_ids[:k]

    is_hit = any(
        chunk_id in expected_chunk_ids
        for chunk_id in top_k_chunk_ids
    )

    if is_hit:
        return 1.0

    return 0.0


def calculate_reciprocal_rank_at_k(
    expected_chunk_ids: list[str],
    returned_chunk_ids: list[str],
    k: int,
) -> float:
    """Calculates Reciprocal Rank@K for one question.

    If the first correct chunk is at rank 1 -> 1.0
    If the first correct chunk is at rank 2 -> 0.5
    If the first correct chunk is at rank 5 -> 0.2
    If no correct chunk is found in top K -> 0.0 """

    top_k_chunk_ids = returned_chunk_ids[:k]

    for index, chunk_id in enumerate(top_k_chunk_ids, start=1):
        if chunk_id in expected_chunk_ids:
            return 1.0 / index

    return 0.0


def calculate_recall_at_k(
    expected_chunk_ids: list[str],
    returned_chunk_ids: list[str],
    k: int,
) -> float:
    """Calculates Recall@K.
    Recall@K = found expected chunks / all expected chunks. """

    if not expected_chunk_ids:
        return 0.0

    top_k_chunk_ids = set(returned_chunk_ids[:k])
    expected_chunk_ids_set = set(expected_chunk_ids)

    found_expected_chunk_ids = expected_chunk_ids_set.intersection(
        top_k_chunk_ids
    )

    return len(found_expected_chunk_ids) / len(expected_chunk_ids_set)


def calculate_retrieval_metrics(
    expected_chunk_ids: list[str],
    returned_chunk_ids: list[str],
    k: int,
) -> RetrievalMetrics:
    """ Calculates all retrieval metrics for one question."""

    return RetrievalMetrics(
        hit_at_1=calculate_hit_at_1(
            expected_chunk_ids=expected_chunk_ids,
            returned_chunk_ids=returned_chunk_ids,
        ),
        hit_at_k=calculate_hit_at_k(
            expected_chunk_ids=expected_chunk_ids,
            returned_chunk_ids=returned_chunk_ids,
            k=k,
        ),
        reciprocal_rank_at_k=calculate_reciprocal_rank_at_k(
            expected_chunk_ids=expected_chunk_ids,
            returned_chunk_ids=returned_chunk_ids,
            k=k,
        ),
        recall_at_k=calculate_recall_at_k(
            expected_chunk_ids=expected_chunk_ids,
            returned_chunk_ids=returned_chunk_ids,
            k=k,
        ),
    )