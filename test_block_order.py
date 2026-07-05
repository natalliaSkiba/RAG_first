from pathlib import Path

from src.chunking.markdown_parser import parse_markdown
from src.chunking.section_builder import build_sections


file_path = Path("data/cleaned/amv_011_015.md")

markdown_text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(markdown_text)
sections = build_sections(blocks)

section = sections[0]

print("Section:", section.section_id)
print("Heading path:", section.heading_path)
print()

for index, block in enumerate(section.blocks, start=1):
    print(
        f"{index}. "
        f"type={block.block_type}, "
        f"start={block.start_char}, "
        f"end={block.end_char}"
    )

    if block.block_type == "image":
        print("   image:", block.image_path)
    else:
        preview = block.text.replace("\n", " ")[:120]
        print("   text:", preview)

    print()