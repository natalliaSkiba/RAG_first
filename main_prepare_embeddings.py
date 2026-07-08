import json
from pathlib import Path

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.reader import (
    count_chunks_by_file,
    read_chunks_from_folder,
    read_chunks_from_jsonl,
)
from src.embedding.writer import (
    build_embedding_output_file,
    create_empty_embedding_records,
    write_embedding_records_to_jsonl,
)


input_folder = Path("data/chunks")
output_folder = Path("data/embeddings")
expected_chunks = 455

output_folder.mkdir(
    parents=True,
    exist_ok=True,
)

config = DEFAULT_EMBEDDING_CONFIG
chunks = read_chunks_from_folder(input_folder)
counts_by_file = count_chunks_by_file(input_folder)

total_chunks = len(chunks)

print("Embedding preparation")
print(f"Provider: {config.provider}")
print(f"Model: {config.model_name}")
print(f"Dimension: {config.dimension}")
print(f"Input folder: {input_folder}")
print(f"Output folder: {output_folder}")
print()

for file_name, count in counts_by_file.items():
    print(f"{file_name}: {count} chunks")

print()
print(f"Total chunks: {total_chunks}")

if total_chunks != expected_chunks:
    raise SystemExit(
        f"Expected {expected_chunks} chunks, got {total_chunks}"
    )

print()
print("Writing empty embedding structure...")

written_records = 0

for input_file in sorted(input_folder.glob("*.jsonl")):
    file_chunks = read_chunks_from_jsonl(input_file)

    empty_embedding_records = create_empty_embedding_records(
        chunks=file_chunks,
        config=config,
    )

    output_file = build_embedding_output_file(
        input_file=input_file,
        output_folder=output_folder,
    )

    write_embedding_records_to_jsonl(
        records=empty_embedding_records,
        output_file=output_file,
    )

    written_records += len(empty_embedding_records)

    print(
        f"{output_file.name}: "
        f"{len(empty_embedding_records)} records"
    )

if written_records != expected_chunks:
    raise SystemExit(
        f"Expected to write {expected_chunks} records, "
        f"wrote {written_records}"
    )

first_record = create_empty_embedding_records(
    chunks=[chunks[0]],
    config=config,
)[0]

print()
print("Output structure preview:")
print(
    json.dumps(
        first_record.to_dict(),
        ensure_ascii=False,
        indent=2,
    )[:1000]
)

print()
print(f"Written embedding records: {written_records}")
print("Embedding preparation completed.")