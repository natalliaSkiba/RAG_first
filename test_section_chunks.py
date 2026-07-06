from pathlib import Path

from src.chunking.chunker import create_chunks_from_section
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections


file_path = Path("data/cleaned/amv_011_015.md")

markdown_text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(markdown_text)
sections = build_sections(blocks)

chunks = create_chunks_from_section(
    section=sections[0],
    source=file_path.name,
    start_chunk_number=1,
)

print("Chunks:", len(chunks))

for chunk in chunks:
    print(
        f"{chunk.chunk_id}: "
        f"text={len(chunk.text)}, "
        f"images={len(chunk.metadata.images)}, "
        f"type={chunk.metadata.chunk_type}"
    )

    for image in chunk.metadata.images:
        print("   ", image)