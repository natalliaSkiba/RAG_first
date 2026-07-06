from pathlib import Path

from src.chunking.chunker import create_text_parts
from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections


file_path = Path("data/cleaned/amv_011_015.md")

markdown_text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(markdown_text)
sections = build_sections(blocks)

text_parts = create_text_parts(sections[0])

print("Parts:", len(text_parts))

for part in text_parts:
    print(
        f"Part {part.part_number}: "
        f"text={len(part.text)}, "
        f"images={len(part.images)}, "
        f"type={part.chunk_type}"
    )

    for image in part.images:
        print("   ", image)