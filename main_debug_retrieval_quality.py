from pathlib import Path

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.local_provider import LocalSentenceTransformerProvider
from src.retrieval.query import generate_query_embedding
from src.retrieval.reader import read_embedding_records_from_folder
from src.retrieval.search import dot_product


input_folder = Path("data/embeddings")
question = "Que faire en cas de détresse ?"

keywords = [
    "détresse",
    "detresse",
    "DSEC",
    "secours",
]

expected_chunk_id = "amv_021_025_chunk_0023"

records = read_embedding_records_from_folder(
    input_folder=input_folder,
)

config = DEFAULT_EMBEDDING_CONFIG

provider = LocalSentenceTransformerProvider(
    config=config,
)

query_embedding = generate_query_embedding(
    question=question,
    provider=provider,
)

print("Retrieval quality debug")
print(f"Question: {question}")
print(f"Loaded records: {len(records)}")
print(f"Expected chunk ID: {expected_chunk_id}")
print()

print("Keyword matches:")
print("=" * 80)

keyword_matches = []

for record in records:
    searchable_text = " ".join(
        [
            record.text,
            str(record.metadata.get("heading", "")),
            str(record.metadata.get("source", "")),
        ]
    ).lower()

    matched_keywords = [
        keyword
        for keyword in keywords
        if keyword.lower() in searchable_text
    ]

    if matched_keywords:
        keyword_matches.append(record)

        print(f"ID: {record.chunk_id}")
        print(f"Source: {record.metadata.get('source')}")
        print(f"Heading: {record.metadata.get('heading')}")
        print(f"Matched keywords: {matched_keywords}")
        print(f"Images: {record.get_images()}")
        print("-" * 80)

print()
print(f"Keyword match count: {len(keyword_matches)}")
print()

scored_records = []

for record in records:
    score = dot_product(
        query_embedding,
        record.embedding,
    )

    scored_records.append(
        (
            score,
            record,
        )
    )

scored_records.sort(
    key=lambda item: item[0],
    reverse=True,
)

print("Expected chunk semantic rank:")
print("=" * 80)

for index, (score, record) in enumerate(scored_records, start=1):
    if record.chunk_id == expected_chunk_id:
        print(f"Rank: {index}")
        print(f"Score: {score:.6f}")
        print(f"ID: {record.chunk_id}")
        print(f"Source: {record.metadata.get('source')}")
        print(f"Heading: {record.metadata.get('heading')}")
        print(f"Images: {record.get_images()}")
        print()
        print("Text:")
        print(record.text)
        break
else:
    raise SystemExit(
        f"Expected chunk not found: {expected_chunk_id}"
    )

print()
print("Top 20 semantic results:")
print("=" * 80)

for rank, (score, record) in enumerate(scored_records[:20], start=1):
    print(f"Rank: {rank}")
    print(f"Score: {score:.6f}")
    print(f"ID: {record.chunk_id}")
    print(f"Source: {record.metadata.get('source')}")
    print(f"Heading: {record.metadata.get('heading')}")
    print("-" * 80)

print()
print("Retrieval quality debug completed.")