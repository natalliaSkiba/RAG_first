from pathlib import Path

from src.chunking.chunker import (
    MAX_CHUNK_SIZE,
    create_chunks,
)
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections


cleaned_folder = Path("data/cleaned")

all_chunk_ids: list[str] = []
all_parsed_images: list[str] = []
all_chunk_images: list[str] = []

total_sections = 0
total_chunks = 0
empty_chunks = []
missing_images = []
oversized_text_chunks = []

for file_path in sorted(cleaned_folder.glob("*.md")):
    markdown_text = file_path.read_text(encoding="utf-8")

    blocks = parse_markdown(markdown_text)
    sections = build_sections(blocks)

    chunks = create_chunks(
        sections=sections,
        source=file_path.name,
    )

    parsed_images = [
        block.image_path
        for block in blocks
        if (
            block.block_type == "image"
            and block.image_path is not None
        )
    ]

    chunk_images = [
        image_path
        for chunk in chunks
        for image_path in chunk.metadata.images
    ]

    total_sections += len(sections)
    total_chunks += len(chunks)

    all_chunk_ids.extend(
        chunk.chunk_id
        for chunk in chunks
    )

    all_parsed_images.extend(parsed_images)
    all_chunk_images.extend(chunk_images)

    for chunk in chunks:
        if not chunk.text.strip():
            empty_chunks.append(chunk.chunk_id)

        if (
            len(chunk.text) > MAX_CHUNK_SIZE
            and chunk.metadata.chunk_type != "table"
        ):
            oversized_text_chunks.append(
                (
                    chunk.chunk_id,
                    len(chunk.text),
                    chunk.metadata.chunk_type,
                )
            )

    for image_path in chunk_images:
        if not Path(image_path).exists():
            missing_images.append(image_path)

    print(
        f"{file_path.name}: "
        f"sections={len(sections)}, "
        f"chunks={len(chunks)}, "
        f"images={len(chunk_images)}"
    )

duplicate_chunk_ids = (
    len(all_chunk_ids)
    - len(set(all_chunk_ids))
)

duplicate_image_links = (
    len(all_chunk_images)
    - len(set(all_chunk_images))
)

print()
print("Documents:", len(list(cleaned_folder.glob('*.md'))))
print("Sections:", total_sections)
print("Chunks:", total_chunks)
print("Parsed images:", len(all_parsed_images))
print("Images in chunks:", len(all_chunk_images))
print("Duplicate chunk IDs:", duplicate_chunk_ids)
print("Duplicate image links:", duplicate_image_links)
print("Empty chunks:", len(empty_chunks))
print("Missing image files:", len(missing_images))
print("Oversized text chunks:", len(oversized_text_chunks))

if empty_chunks:
    print("Empty chunk IDs:", empty_chunks)

if missing_images:
    print("Missing images:", missing_images)

if oversized_text_chunks:
    print("Oversized text chunks:")

    for item in oversized_text_chunks:
        print(item)