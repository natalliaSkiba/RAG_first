from pathlib import Path

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.local_provider import LocalSentenceTransformerProvider
from src.retrieval.query import generate_query_embedding
from src.retrieval.reader import read_embedding_records_from_folder
from src.retrieval.search import (
    dot_product,
    search_by_vector_hybrid,
)


input_folder = Path("data/embeddings")

question = "Que faire en cas de détresse ?"
top_k = 5
expected_chunk_id = "amv_021_025_chunk_0023"

config = DEFAULT_EMBEDDING_CONFIG

print("Hybrid semantic search")
print(f"Question: {question}")
print(f"Input folder: {input_folder}")
print(f"Model: {config.model_name}")
print(f"Top-k: {top_k}")
print()

records = read_embedding_records_from_folder(
    input_folder=input_folder,
)

provider = LocalSentenceTransformerProvider(
    config=config,
)

query_embedding = generate_query_embedding(
    question=question,
    provider=provider,
)

results = search_by_vector_hybrid(
    question=question,
    query_embedding=query_embedding,
    records=records,
    top_k=top_k,
)

print(f"Loaded records: {len(records)}")
print(f"Query embedding dimension: {len(query_embedding)}")
print()

print("Top hybrid results:")
print("=" * 80)

for result in results:
    record = result.record
    metadata = record.metadata

    text_preview = record.text.replace("\n", " ")
    text_preview = text_preview[:700]

    print(f"Rank: {result.rank}")
    print(f"Final score: {result.score:.6f}")
    print(f"Semantic score: {result.semantic_score:.6f}")
    print(f"Keyword score: {result.keyword_score:.6f}")
    print(f"ID: {record.chunk_id}")
    print(f"Source: {metadata.get('source')}")
    print(f"Heading: {metadata.get('heading')}")
    print(f"Chunk type: {metadata.get('chunk_type')}")
    print(f"Images: {record.get_images()}")
    print()
    print("Text preview:")
    print(text_preview)
    print("-" * 80)

scored_records = []

for record in records:
    semantic_score = dot_product(
        query_embedding,
        record.embedding,
    )

    keyword_score = 0.0

    for result in search_by_vector_hybrid(
        question=question,
        query_embedding=query_embedding,
        records=[record],
        top_k=1,
    ):
        keyword_score = result.keyword_score

    final_score = semantic_score + keyword_score

    scored_records.append(
        (
            final_score,
            semantic_score,
            keyword_score,
            record,
        )
    )

scored_records.sort(
    key=lambda item: item[0],
    reverse=True,
)

print()
print("Expected chunk hybrid rank:")
print("=" * 80)

for index, (
    final_score,
    semantic_score,
    keyword_score,
    record,
) in enumerate(scored_records, start=1):
    if record.chunk_id == expected_chunk_id:
        print(f"Rank: {index}")
        print(f"Final score: {final_score:.6f}")
        print(f"Semantic score: {semantic_score:.6f}")
        print(f"Keyword score: {keyword_score:.6f}")
        print(f"ID: {record.chunk_id}")
        print(f"Source: {record.metadata.get('source')}")
        print(f"Heading: {record.metadata.get('heading')}")
        print(f"Images: {record.get_images()}")
        break

print()
print("Hybrid semantic search completed.")