from pathlib import Path

from src.chunking.chunker import (
    build_section_text,
    get_section_images,
)
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections


file_path = Path("data/cleaned/amv_011_015.md")

markdown_text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(markdown_text)
sections = build_sections(blocks)

section_with_images = next(
    section
    for section in sections
    if get_section_images(section)
)

section_text = build_section_text(section_with_images)
section_images = get_section_images(section_with_images)

print("Section ID:", section_with_images.section_id)
print("Text length:", len(section_text))
print("Images:", len(section_images))
print("First image:", section_images[0])