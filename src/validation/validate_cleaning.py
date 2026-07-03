from pathlib import Path


def get_markdown_filenames(folder: Path) -> set[str]:
    """Returns names of all Markdown files in a folder."""

    if not folder.exists():
        raise FileNotFoundError(
            f"Folder does not exist: {folder}"
        )

    return {
        file.name
        for file in folder.glob("*.md")
    }


def compare_filenames(
    extracted_folder: Path,
    cleaned_folder: Path,
) -> tuple[set[str], set[str]]:
    """Compares filenames in extracted and cleaned folders."""

    extracted_files = get_markdown_filenames(extracted_folder)
    cleaned_files = get_markdown_filenames(cleaned_folder)

    missing_files = extracted_files - cleaned_files
    extra_files = cleaned_files - extracted_files

    return missing_files, extra_files

def find_empty_files(folder: Path) -> list[str]:
    """Returns names of empty Markdown files."""

    empty_files = []

    for file in folder.glob("*.md"):
        text = file.read_text(encoding="utf-8")

        if not text.strip():
            empty_files.append(file.name)

    return empty_files

def find_files_containing(
    folder: Path,
    fragment: str,
) -> list[str]:
    """Returns names of files containing the specified fragment."""

    matching_files = []

    for file in folder.glob("*.md"):
        text = file.read_text(encoding="utf-8")

        if fragment in text:
            matching_files.append(file.name)

    return matching_files


def compare_fragment_counts(
    extracted_folder: Path,
    cleaned_folder: Path,
    fragment: str,
) -> dict[str, tuple[int, int]]:
    """Compares fragment counts in extracted and cleaned files."""

    differences = {}

    for extracted_file in extracted_folder.glob("*.md"):
        cleaned_file = cleaned_folder / extracted_file.name

        if not cleaned_file.exists():
            continue

        extracted_text = extracted_file.read_text(encoding="utf-8")
        cleaned_text = cleaned_file.read_text(encoding="utf-8")

        extracted_count = extracted_text.count(fragment)
        cleaned_count = cleaned_text.count(fragment)

        if extracted_count != cleaned_count:
            differences[extracted_file.name] = (
                extracted_count,
                cleaned_count,
            )

    return differences