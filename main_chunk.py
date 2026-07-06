from pathlib import Path

from src.chunking.chunker import create_chunks
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections
from src.chunking.writer import write_chunks_to_jsonl
from src.validation.validate_chunking import validate_chunks


input_folder = Path("data/cleaned")
output_folder = Path("data/chunks")

output_folder.mkdir(
    parents=True,
    exist_ok=True,
)

total_documents = 0
total_chunks = 0
all_errors: list[str] = []

for input_file in sorted(input_folder.glob("*.md")):
    markdown_text = input_file.read_text(
        encoding="utf-8",
    )

    blocks = parse_markdown(markdown_text)
    sections = build_sections(blocks)

    chunks = create_chunks(
        sections=sections,
        source=input_file.name,
    )

    errors = validate_chunks(chunks)

    if errors:
        all_errors.extend(errors)
        print(f"Validation failed: {input_file.name}")

        for error in errors:
            print(f"  - {error}")

        continue

    output_file = output_folder / f"{input_file.stem}.jsonl"

    write_chunks_to_jsonl(
        chunks=chunks,
        output_file=output_file,
    )

    total_documents += 1
    total_chunks += len(chunks)

    print(
        f"Chunked: {input_file.name} "
        f"-> {output_file.name} "
        f"({len(chunks)} chunks)"
    )

if all_errors:
    print()
    print("Chunking completed with validation errors.")
    print(f"Errors: {len(all_errors)}")
    raise SystemExit(1)

print()
print("Chunking completed.")
print(f"Documents: {total_documents}")
print(f"Chunks: {total_chunks}")