from pathlib import Path

from src.chunking.markdown_parser import parse_markdown


file_path = Path("data/cleaned/amv_011_015.md")

text = file_path.read_text(encoding="utf-8")

blocks = parse_markdown(text)

images = [
    block
    for block in blocks
    if block.block_type == "image"
]

print("Images:", len(images))

if images:
    print(images[0])
