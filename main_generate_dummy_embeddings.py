from pathlib import Path

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.generator import generate_embedding_records
from src.embedding.provider import DummyEmbeddingProvider
from src.embedding.reader import read_chunks_from_jsonl
from src.embedding.writer import (
    build_embedding_output_file,
    write_embedding_records_to_jsonl,
)


input_folder = Path("data/chunks")
output_folder = Path("data/embeddings")
expected_chunks = 455

config = DEFAULT_EMBEDDING_CONFIG

provider = DummyEmbeddingProvider(
    config=config,
)

output_folder.mkdir(
    parents=True,
    exist_ok=True,
)

print("Dummy embedding generation")
print(f"Provider: {config.provider}")
print(f"Model: {config.model_name}")
print(f"Dimension: {config.dimension}")
print(f"Input folder: {input_folder}")
print(f"Output folder: {output_folder}")
print()

total_records = 0

for input_file in sorted(input_folder.glob("*.jsonl")):
    chunks = read_chunks_from_jsonl(input_file)

    embedding_records = generate_embedding_records(
        chunks=chunks,
        provider=provider,
    )

    output_file = build_embedding_output_file(
        input_file=input_file,
        output_folder=output_folder,
    )

    write_embedding_records_to_jsonl(
        records=embedding_records,
        output_file=output_file,
    )

    total_records += len(embedding_records)

    print(
        f"{output_file.name}: "
        f"{len(embedding_records)} records"
    )

print()
print(f"Total generated records: {total_records}")

if total_records != expected_chunks:
    raise SystemExit(
        f"Expected {expected_chunks} records, got {total_records}"
    )

print("Dummy embedding generation completed.")