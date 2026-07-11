from pathlib import Path

from src.retrieval.reader import read_embedding_records_from_folder


input_folder = Path("data/embeddings")
output_file = Path("data/evaluation/retrieval_candidates.md")

records = read_embedding_records_from_folder(
    input_folder=input_folder,
)

output_file.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with output_file.open(
    mode="w",
    encoding="utf-8",
) as file:
    file.write("# Retrieval candidates\n\n")
    file.write(
        "This file helps select evaluation questions from real chunks.\n\n"
    )

    for record in records:
        metadata = record.metadata

        heading = metadata.get("heading", "")
        source = metadata.get("source", "")
        chunk_type = metadata.get("chunk_type", "")
        images = record.get_images()

        text_preview = record.text.replace("\n", " ")
        text_preview = text_preview[:500]

        file.write(f"## {record.chunk_id}\n\n")
        file.write(f"- Source: `{source}`\n")
        file.write(f"- Heading: {heading}\n")
        file.write(f"- Chunk type: `{chunk_type}`\n")
        file.write(f"- Images: {len(images)}\n")
        file.write("\n")
        file.write("Preview:\n\n")
        file.write(f"> {text_preview}\n\n")
        file.write("---\n\n")

print("Retrieval candidates export")
print(f"Input folder: {input_folder}")
print(f"Loaded records: {len(records)}")
print(f"Output file: {output_file}")
print("Retrieval candidates export completed.")