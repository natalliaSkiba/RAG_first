from pathlib import Path

from src.chunking.chunker import create_chunk_from_section
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections


file_path = Path("data/cleaned/amv_011_015.md")

markdown_text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(markdown_text)
sections = build_sections(blocks)

chunk = create_chunk_from_section(
    section=sections[0],
    source=file_path.name,
    chunk_number=1,
)

print("Chunk ID:", chunk.chunk_id)
print("Text length:", len(chunk.text))
print("Heading:", chunk.metadata.heading)
print("Chunk type:", chunk.metadata.chunk_type)
print("Images:", chunk.metadata.images)