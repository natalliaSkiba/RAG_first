from pathlib import Path

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.local_provider import LocalSentenceTransformerProvider
from src.retrieval.evaluation import (
    RetrievalTestCase,
    evaluate_retrieval_result,
)
from src.retrieval.query import generate_query_embedding
from src.retrieval.reader import read_embedding_records_from_folder
from src.retrieval.search import search_by_vector_hybrid


input_folder = Path("data/embeddings")
top_k = 5

test_cases = [
    RetrievalTestCase(
        question="Que faire en cas de détresse ?",
        expected_chunk_ids=[
            "amv_021_025_chunk_0023",
            "amv_021_025_chunk_0024",
            "amv_021_025_chunk_0025",
        ],
    ),
    RetrievalTestCase(
        question="Que faire avant de traverser une voie ?",
        expected_chunk_ids=[
            "amv_061_065_chunk_0020",
            "amv_061_065_chunk_0021",
        ],
    ),
    RetrievalTestCase(
        question="Que faire en cas d'accident électrique impliquant une personne ?",
        expected_chunk_ids=[
            "amv_061_065_chunk_0033",
        ],
    ),
    RetrievalTestCase(
        question="Que faire en cas de réalimentation en secours ?",
        expected_chunk_ids=[
            "amv_041_045_chunk_0014",
            "amv_041_045_chunk_0023",
            "amv_041_045_chunk_0024",
        ],
    ),
]

config = DEFAULT_EMBEDDING_CONFIG

print("Retrieval evaluation")
print(f"Input folder: {input_folder}")
print(f"Model: {config.model_name}")
print(f"Top-k: {top_k}")
print(f"Test cases: {len(test_cases)}")
print()

records = read_embedding_records_from_folder(
    input_folder=input_folder,
)

provider = LocalSentenceTransformerProvider(
    config=config,
)

evaluation_results = []

for test_case in test_cases:
    query_embedding = generate_query_embedding(
        question=test_case.question,
        provider=provider,
    )

    search_results = search_by_vector_hybrid(
        question=test_case.question,
        query_embedding=query_embedding,
        records=records,
        top_k=top_k,
    )

    evaluation_result = evaluate_retrieval_result(
        question=test_case.question,
        expected_chunk_ids=test_case.expected_chunk_ids,
        search_results=search_results,
    )

    evaluation_results.append(evaluation_result)

    status = "PASS" if evaluation_result.is_success else "FAIL"

    print("=" * 80)
    print(f"Question: {test_case.question}")
    print(f"Status: {status}")
    print(f"Expected: {test_case.expected_chunk_ids}")
    print(f"Returned: {evaluation_result.returned_chunk_ids}")
    print()

    print("Top results:")
    for result in search_results:
        print(
            f"- Rank {result.rank}: "
            f"{result.record.chunk_id} | "
            f"final={result.score:.6f} | "
            f"semantic={result.semantic_score:.6f} | "
            f"keyword={result.keyword_score:.6f} | "
            f"heading={result.record.metadata.get('heading')}"
        )

    print()

success_count = sum(
    1 for result in evaluation_results if result.is_success
)

total_count = len(evaluation_results)

print("=" * 80)
print("Evaluation summary")
print(f"Success: {success_count}/{total_count}")
print(f"Accuracy@{top_k}: {success_count / total_count:.2%}")

if success_count != total_count:
    raise SystemExit(
        "Retrieval evaluation failed: "
        f"{success_count}/{total_count} test cases passed"
    )

print("Retrieval evaluation completed.")