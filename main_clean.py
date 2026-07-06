from pathlib import Path

from src.cleaning.rules import clean_text


input_folder = Path("data/extracted")
output_folder = Path("data/cleaned")

output_folder.mkdir(parents=True, exist_ok=True)

for file_path in input_folder.glob("*.md"):
    raw_text = file_path.read_text(encoding="utf-8")

    source_stem = file_path.stem.removeprefix("amv_")

    cleaned_text = clean_text(
        text=raw_text,
        source_stem=source_stem,
    )

    output_file = output_folder / file_path.name

    output_file.write_text(
        cleaned_text,
        encoding="utf-8",
    )

    print(f"Cleaned: {file_path.name}")

print("Cleaning completed.")