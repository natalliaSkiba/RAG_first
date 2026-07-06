from pathlib import Path

from src.chunking.chunker import create_chunks
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections
from src.chunking.writer import write_chunks_to_jsonl
from src.validation.validate_chunking import validate_chunks


input_file = Path("data/cleaned/amv_011_015.md")
output_file = Path("data/chunks/amv_011_015.jsonl")

markdown_text = input_file.read_text(encoding="utf-8")

blocks = parse_markdown(markdown_text)
sections = build_sections(blocks)

chunks = create_chunks(
    sections=sections,
    source=input_file.name,
)

errors = validate_chunks(chunks)

if errors:
    print("Validation errors:")

    for error in errors:
        print(error)

    raise SystemExit(1)

write_chunks_to_jsonl(
    chunks=chunks,
    output_file=output_file,
)

print("Chunks:", len(chunks))
print("Written to:", output_file)