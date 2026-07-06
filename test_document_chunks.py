from pathlib import Path

from src.chunking.chunker import create_chunks
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections


file_path = Path("data/cleaned/amv_011_015.md")

markdown_text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(markdown_text)
sections = build_sections(blocks)

chunks = create_chunks(
    sections=sections,
    source=file_path.name,
)

chunks_with_images = [
    chunk
    for chunk in chunks
    if chunk.metadata.images
]

empty_chunks = [
    chunk
    for chunk in chunks
    if not chunk.text.strip()
]

print("Sections:", len(sections))
print("Chunks:", len(chunks))
print("Chunks with images:", len(chunks_with_images))
print("Empty chunks:", len(empty_chunks))

if chunks:
    print("First chunk:", chunks[0].chunk_id)
    print("Last chunk:", chunks[-1].chunk_id)

for chunk in chunks_with_images:
    print(
        f"{chunk.chunk_id}: "
        f"images={len(chunk.metadata.images)}, "
        f"heading={chunk.metadata.heading}"
    )

print("\nEmpty chunk details:")

for chunk in empty_chunks:
    print("ID:", chunk.chunk_id)
    print("Section:", chunk.metadata.section_id)
    print("Heading:", chunk.metadata.heading)
    print("Type:", chunk.metadata.chunk_type)
    print("Images:", chunk.metadata.images)