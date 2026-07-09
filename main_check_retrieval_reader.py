from pathlib import Path

from src.retrieval.reader import (
    count_embedding_records_by_file,
    read_embedding_records_from_folder,
)


input_folder = Path("data/embeddings")
expected_records = 455

records = read_embedding_records_from_folder(
    input_folder=input_folder,
)

counts_by_file = count_embedding_records_by_file(
    input_folder=input_folder,
)

records_with_images = sum(
    1 for record in records if record.get_images()
)

print("Retrieval reader check")
print(f"Input folder: {input_folder}")
print(f"Embedding files: {len(counts_by_file)}")
print(f"Expected records: {expected_records}")
print(f"Loaded records: {len(records)}")
print(f"Records with images: {records_with_images}")
print()

if len(records) != expected_records:
    raise SystemExit(
        f"Expected {expected_records} records, got {len(records)}"
    )

first_record = records[0]

print("First record:")
print(f"ID: {first_record.chunk_id}")
print(f"Text length: {len(first_record.text)}")
print(f"Embedding dimension: {len(first_record.embedding)}")
print(f"Source: {first_record.metadata.get('source')}")
print(f"Images: {first_record.get_images()}")
print()

print("Records by file:")
for file_name, count in counts_by_file.items():
    print(f"- {file_name}: {count}")

print()
print("Retrieval reader check completed.")