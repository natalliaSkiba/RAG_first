from pathlib import Path

from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections


file_path = Path("data/cleaned/amv_011_015.md")

text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(text)

sections = build_sections(blocks)

image_sections = []

for section in sections:
    images = [
        block.image_path
        for block in section.blocks
        if block.block_type == "image"
    ]

    if images:
        image_sections.append((section, images))

print("Sections:", len(sections))
print("Sections with images:", len(image_sections))

if image_sections:
    first_section, first_images = image_sections[0]
    print("Section ID:", first_section.section_id)
    print("Heading path:", first_section.heading_path)
    print("Images in first image section:", len(first_images))
    print("First image path:", first_images[0])