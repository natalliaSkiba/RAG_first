from pathlib import Path

from src.chunking.chunker import (
    build_section_text,
    split_text_by_size,
)
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections


file_path = Path("data/cleaned/amv_011_015.md")

markdown_text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(markdown_text)
sections = build_sections(blocks)

section_text = build_section_text(sections[0])

text_parts = split_text_by_size(section_text)

print("Original length:", len(section_text))
print("Parts:", len(text_parts))

for number, text_part in enumerate(text_parts, start=1):
    print(
        f"Part {number}: "
        f"{len(text_part)} characters"
    )