from pathlib import Path

from src.retrieval.reader import read_embedding_records_from_folder
from src.retrieval.search import search_by_vector


input_folder = Path("data/embeddings")
top_k = 5

records = read_embedding_records_from_folder(
    input_folder=input_folder,
)

query_record = records[0]

results = search_by_vector(
    query_embedding=query_record.embedding,
    records=records,
    top_k=top_k,
)

print("Retrieval vector search self-test")
print(f"Input folder: {input_folder}")
print(f"Loaded records: {len(records)}")
print(f"Query record ID: {query_record.chunk_id}")
print(f"Top-k: {top_k}")
print()

for result in results:
    record = result.record
    metadata = record.metadata

    text_preview = record.text.replace("\n", " ")
    text_preview = text_preview[:250]

    print(f"Rank: {result.rank}")
    print(f"Score: {result.score:.6f}")
    print(f"ID: {record.chunk_id}")
    print(f"Source: {metadata.get('source')}")
    print(f"Heading: {metadata.get('heading')}")
    print(f"Chunk type: {metadata.get('chunk_type')}")
    print(f"Images: {record.get_images()}")
    print(f"Text preview: {text_preview}")
    print("-" * 80)

best_result = results[0]

if best_result.record.chunk_id != query_record.chunk_id:
    raise SystemExit(
        "Self-test failed: first result is not the query record itself. "
        f"Expected {query_record.chunk_id}, "
        f"got {best_result.record.chunk_id}"
    )

print()
print("Retrieval vector search self-test completed.")