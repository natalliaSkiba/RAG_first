from pathlib import Path

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.local_provider import LocalSentenceTransformerProvider
from src.retrieval.evaluation import (
    calculate_retrieval_metrics,
    evaluate_retrieval_result,
    extract_chunk_ids_from_search_results,
    load_retrieval_test_cases,
)
from src.retrieval.query import generate_query_embedding
from src.retrieval.reader import read_embedding_records_from_folder
from src.retrieval.search import (
    search_by_vector,
    search_by_vector_hybrid,
)


input_folder = Path("data/embeddings")
test_cases_file = Path("data/evaluation/retrieval_test_cases.json")
top_k = 5

config = DEFAULT_EMBEDDING_CONFIG

print("Retrieval evaluation")
print(f"Input folder: {input_folder}")
print(f"Test cases file: {test_cases_file}")
print(f"Model: {config.model_name}")
print(f"Top-k: {top_k}")
print()

records = read_embedding_records_from_folder(
    input_folder=input_folder,
)

test_cases = load_retrieval_test_cases(
    file_path=test_cases_file,
)

provider = LocalSentenceTransformerProvider(
    config=config,
)

semantic_metrics_results = []
hybrid_metrics_results = []
hybrid_evaluation_results = []

for test_case in test_cases:
    query_embedding = generate_query_embedding(
        question=test_case.question,
        provider=provider,
    )

    semantic_results = search_by_vector(
        query_embedding=query_embedding,
        records=records,
        top_k=top_k,
    )

    hybrid_results = search_by_vector_hybrid(
        question=test_case.question,
        query_embedding=query_embedding,
        records=records,
        top_k=top_k,
    )

    semantic_returned_chunk_ids = extract_chunk_ids_from_search_results(
        search_results=semantic_results,
    )

    hybrid_returned_chunk_ids = extract_chunk_ids_from_search_results(
        search_results=hybrid_results,
    )

    semantic_metrics = calculate_retrieval_metrics(
        expected_chunk_ids=test_case.expected_chunk_ids,
        returned_chunk_ids=semantic_returned_chunk_ids,
        k=top_k,
    )

    hybrid_metrics = calculate_retrieval_metrics(
        expected_chunk_ids=test_case.expected_chunk_ids,
        returned_chunk_ids=hybrid_returned_chunk_ids,
        k=top_k,
    )

    hybrid_evaluation_result = evaluate_retrieval_result(
        question=test_case.question,
        expected_chunk_ids=test_case.expected_chunk_ids,
        returned_chunk_ids=hybrid_returned_chunk_ids,
    )

    semantic_metrics_results.append(semantic_metrics)
    hybrid_metrics_results.append(hybrid_metrics)
    hybrid_evaluation_results.append(hybrid_evaluation_result)

    status = "PASS" if hybrid_evaluation_result.is_success else "FAIL"

    print("=" * 80)
    print(f"Question: {test_case.question}")
    print(f"Topic: {test_case.topic}")
    print(f"Hybrid status: {status}")
    print(f"Expected: {test_case.expected_chunk_ids}")
    print(f"Notes: {test_case.notes}")
    print()

    print("Semantic metrics:")
    print(f"Hit@1: {semantic_metrics.hit_at_1:.2f}")
    print(f"Hit@{top_k}: {semantic_metrics.hit_at_k:.2f}")
    print(
        f"ReciprocalRank@{top_k}: "
        f"{semantic_metrics.reciprocal_rank_at_k:.2f}"
    )
    print(f"Recall@{top_k}: {semantic_metrics.recall_at_k:.2f}")
    print(f"Returned: {semantic_returned_chunk_ids}")
    print()

    print("Hybrid metrics:")
    print(f"Hit@1: {hybrid_metrics.hit_at_1:.2f}")
    print(f"Hit@{top_k}: {hybrid_metrics.hit_at_k:.2f}")
    print(
        f"ReciprocalRank@{top_k}: "
        f"{hybrid_metrics.reciprocal_rank_at_k:.2f}"
    )
    print(f"Recall@{top_k}: {hybrid_metrics.recall_at_k:.2f}")
    print(f"Returned: {hybrid_returned_chunk_ids}")
    print()

    print("Top hybrid results:")
    for result in hybrid_results:
        print(
            f"- Rank {result.rank}: "
            f"{result.record.chunk_id} | "
            f"final={result.score:.6f} | "
            f"semantic={result.semantic_score:.6f} | "
            f"keyword={result.keyword_score:.6f} | "
            f"heading={result.record.metadata.get('heading')}"
        )

    print()


def calculate_mean_metric(
    values: list[float],
) -> float:
    """
    Calculates mean value.

    Считает среднее значение.
    """

    if not values:
        return 0.0

    return sum(values) / len(values)


total_count = len(test_cases)

semantic_hit_at_1 = calculate_mean_metric(
    [metrics.hit_at_1 for metrics in semantic_metrics_results]
)

semantic_hit_at_k = calculate_mean_metric(
    [metrics.hit_at_k for metrics in semantic_metrics_results]
)

semantic_mrr_at_k = calculate_mean_metric(
    [
        metrics.reciprocal_rank_at_k
        for metrics in semantic_metrics_results
    ]
)

semantic_recall_at_k = calculate_mean_metric(
    [metrics.recall_at_k for metrics in semantic_metrics_results]
)

hybrid_hit_at_1 = calculate_mean_metric(
    [metrics.hit_at_1 for metrics in hybrid_metrics_results]
)

hybrid_hit_at_k = calculate_mean_metric(
    [metrics.hit_at_k for metrics in hybrid_metrics_results]
)

hybrid_mrr_at_k = calculate_mean_metric(
    [
        metrics.reciprocal_rank_at_k
        for metrics in hybrid_metrics_results
    ]
)

hybrid_recall_at_k = calculate_mean_metric(
    [metrics.recall_at_k for metrics in hybrid_metrics_results]
)

hybrid_success_count = sum(
    1 for result in hybrid_evaluation_results if result.is_success
)

print("=" * 80)
print("Evaluation summary")
print(f"Questions: {total_count}")
print()

print("Semantic search:")
print(f"Hit@1: {semantic_hit_at_1:.2%}")
print(f"Hit@{top_k}: {semantic_hit_at_k:.2%}")
print(f"MRR@{top_k}: {semantic_mrr_at_k:.2%}")
print(f"Recall@{top_k}: {semantic_recall_at_k:.2%}")
print()

print("Hybrid search:")
print(f"Success: {hybrid_success_count}/{total_count}")
print(f"Hit@1: {hybrid_hit_at_1:.2%}")
print(f"Hit@{top_k}: {hybrid_hit_at_k:.2%}")
print(f"MRR@{top_k}: {hybrid_mrr_at_k:.2%}")
print(f"Recall@{top_k}: {hybrid_recall_at_k:.2%}")

if hybrid_success_count != total_count:
    raise SystemExit(
        "Hybrid retrieval evaluation failed: "
        f"{hybrid_success_count}/{total_count} test cases passed"
    )

print("Retrieval evaluation completed.")