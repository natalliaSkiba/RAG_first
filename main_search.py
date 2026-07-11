from pathlib import Path

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.local_provider import LocalSentenceTransformerProvider
from src.retrieval.query import generate_query_embedding
from src.retrieval.reader import read_embedding_records_from_folder
from src.retrieval.search import search_by_vector


input_folder = Path("data/embeddings")

question = "Que faire en cas de détresse ?"
top_k = 5

config = DEFAULT_EMBEDDING_CONFIG

print("Semantic search")
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

results = search_by_vector(
    query_embedding=query_embedding,
    records=records,
    top_k=top_k,
)

print(f"Loaded records: {len(records)}")
print(f"Query embedding dimension: {len(query_embedding)}")
print()

print("Top results:")
print("=" * 80)

for result in results:
    record = result.record
    metadata = record.metadata

    text_preview = record.text.replace("\n", " ")
    text_preview = text_preview[:700]

    print(f"Rank: {result.rank}")
    print(f"Score: {result.score:.6f}")
    print(f"ID: {record.chunk_id}")
    print(f"Source: {metadata.get('source')}")
    print(f"Heading: {metadata.get('heading')}")
    print(f"Chunk type: {metadata.get('chunk_type')}")
    print(f"Images: {record.get_images()}")
    print()
    print("Text preview:")
    print(text_preview)
    print("-" * 80)

print()
print("Semantic search completed.")