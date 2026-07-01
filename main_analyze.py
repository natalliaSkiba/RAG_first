from pathlib import Path
from collections import Counter
from src.analysis.analyze_ocr import load_markdown_previews, count_characters, build_frequency_dictionary,build_word_frequency,find_suspicious_tokens


## Path configurations
input_folder = Path("data/extracted")
report_file = Path("data/reports/ocr_analysis_report.md")

## Get quantity of names , all names of files and first 100 characters per  file
preview_docs = load_markdown_previews(input_folder)

file_lengths = {}
total_chars_sum = 0
global_character_counter = Counter()
global_word_counter = Counter()
global_suspicious_counter = Counter()

## Read every file completely
for file_path in input_folder.glob("*.md"):
    full_text = file_path.read_text(encoding="utf-8")

    ## Characters statistic
    char_count =len(full_text)
    file_lengths[file_path.name] = char_count
    total_chars_sum += char_count

    ## Gathering data of frequency dictionary
    global_character_counter.update(
        count_characters(full_text)
    )

    # Word statistic
    global_word_counter.update(
        build_word_frequency(full_text)
    )

    # Suspicious statistic
    suspicious_tokens = find_suspicious_tokens(full_text)

    global_suspicious_counter.update(
        token.lower() for token in suspicious_tokens
    )

character_frequency = build_frequency_dictionary(
    global_character_counter
)

## REPORT TEXT ASSEMBLY
report_lines = [
    "# OCR Analysis Report",
    "",
    "## 1. First 100 characters",
    ""
]
for name, preview in preview_docs.items():
    report_lines.append(f"### {name}")
    report_lines.append("")
    report_lines.append(preview.replace("\n", " "))
    report_lines.append("")

report_lines.extend([
    "## 2. Text volume statistics",
    "",
    f"- Total files: {len(file_lengths)}",
    f"- Total characters: {total_chars_sum}",
    "",
    "### Characters per file",
    "",
])

for name, length in file_lengths.items():
    report_lines.append(f"- {name}: {length} characters")

report_lines.extend([
    "",
    "## 3. Character frequency",
    "",
    "| Character | Count |",
    "|---|---:|",
])

for char, count in character_frequency.items():
    report_lines.append(f"| `{repr(char)}` | {count} |")

report_lines.extend([
    "",
    "## 4. Word frequency",
    "",
    "| Word | Count |",
    "|---|---:|",
])

# Only 100 more frequents words
for word, count in global_word_counter.most_common(100):
    report_lines.append(f"| {word} | {count} |")


# Suspicious OCR tokens
report_lines.extend([
    "",
    "## 5. Suspicious OCR tokens",
    "",
    "| Token | Count |",
    "|---|---:|",
])

for token, count in global_suspicious_counter.most_common(100):
    report_lines.append(f"| `{token}` | {count} |")

# Save report
report_file.parent.mkdir(parents=True, exist_ok=True)

report_file.write_text(
    "\n".join(report_lines),
    encoding="utf-8",
)

print(f"Report successfully saved to {report_file}")
