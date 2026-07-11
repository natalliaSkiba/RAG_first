from pathlib import Path

from src.retrieval.evaluation import load_retrieval_test_cases


test_cases_file = Path("data/evaluation/retrieval_test_cases.json")

test_cases = load_retrieval_test_cases(
    file_path=test_cases_file,
)

print("Retrieval test cases check")
print(f"File: {test_cases_file}")
print(f"Loaded test cases: {len(test_cases)}")
print()

for index, test_case in enumerate(test_cases, start=1):
    print(f"#{index}")
    print(f"Question: {test_case.question}")
    print(f"Topic: {test_case.topic}")
    print(f"Expected chunks: {test_case.expected_chunk_ids}")
    print(f"Notes: {test_case.notes}")
    print("-" * 80)

print()
print("Retrieval test cases check completed.")