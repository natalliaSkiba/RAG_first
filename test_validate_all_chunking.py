from pathlib import Path

from src.chunking.chunker import create_chunks
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections
from src.validation.validate_chunking import validate_chunks


cleaned_folder = Path("data/cleaned")

total_documents = 0
total_chunks = 0
all_errors: list[str] = []

for file_path in sorted(cleaned_folder.glob("*.md")):
    markdown_text = file_path.read_text(encoding="utf-8")

    blocks = parse_markdown(markdown_text)
    sections = build_sections(blocks)

    chunks = create_chunks(
        sections=sections,
        source=file_path.name,
    )

    errors = validate_chunks(chunks)

    total_documents += 1
    total_chunks += len(chunks)
    all_errors.extend(errors)

    print(
        f"{file_path.name}: "
        f"chunks={len(chunks)}, "
        f"errors={len(errors)}"
    )

print()
print("Documents:", total_documents)
print("Chunks:", total_chunks)
print("Errors:", len(all_errors))

for error in all_errors:
    print(error)