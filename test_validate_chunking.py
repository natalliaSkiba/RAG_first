from pathlib import Path

from src.chunking.chunker import create_chunks
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections
from src.validation.validate_chunking import validate_chunks


file_path = Path("data/cleaned/amv_011_015.md")

markdown_text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(markdown_text)
sections = build_sections(blocks)

chunks = create_chunks(
    sections=sections,
    source=file_path.name,
)

errors = validate_chunks(chunks)

print("Chunks:", len(chunks))
print("Errors:", len(errors))

for error in errors:
    print(error)