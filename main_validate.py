from pathlib import Path

from src.validation.validate_cleaning import (
    compare_filenames,
    compare_fragment_counts,
    find_empty_files,
    find_files_containing,
    get_markdown_filenames,
)


extracted_folder = Path("data/extracted")
cleaned_folder = Path("data/cleaned")

extracted_files = get_markdown_filenames(extracted_folder)
cleaned_files = get_markdown_filenames(cleaned_folder)

print(f"Extracted files: {len(extracted_files)}")
print(f"Cleaned files: {len(cleaned_files)}")

missing_files, extra_files = compare_filenames(
    extracted_folder,
    cleaned_folder,
)

if missing_files:
    print("ERROR: missing files:")

    for filename in sorted(missing_files):
        print(f"- {filename}")

if extra_files:
    print("ERROR: extra files:")

    for filename in sorted(extra_files):
        print(f"- {filename}")

if not missing_files and not extra_files:
    print("OK: filenames are identical")

empty_files = find_empty_files(cleaned_folder)

if empty_files:
    print("ERROR: empty cleaned files:")

    for filename in sorted(empty_files):
        print(f"- {filename}")
else:
    print("OK: no empty cleaned files")

files_with_tabs = find_files_containing(
    cleaned_folder,
    "\t",
)

if files_with_tabs:
    print("ERROR: tab characters found:")

    for filename in sorted(files_with_tabs):
        print(f"- {filename}")
else:
    print("OK: no tab characters")


files_with_image_markers = find_files_containing(
    cleaned_folder,
    "<!-- image -->",
)

if files_with_image_markers:
    print("ERROR: image markers found:")

    for filename in sorted(files_with_image_markers):
        print(f"- {filename}")
else:
    print("OK: no image markers")

heading_differences = compare_fragment_counts(
    extracted_folder,
    cleaned_folder,
    "#",
)

if heading_differences:
    print("ERROR: Markdown heading markers changed:")

    for filename, counts in sorted(heading_differences.items()):
        print(
            f"- {filename}: "
            f"extracted={counts[0]}, cleaned={counts[1]}"
        )
else:
    print("OK: Markdown heading markers are preserved")


table_differences = compare_fragment_counts(
    extracted_folder,
    cleaned_folder,
    "|",
)

if table_differences:
    print("ERROR: Markdown table markers changed:")

    for filename, counts in sorted(table_differences.items()):
        print(
            f"- {filename}: "
            f"extracted={counts[0]}, cleaned={counts[1]}"
        )
else:
    print("OK: Markdown table markers are preserved")