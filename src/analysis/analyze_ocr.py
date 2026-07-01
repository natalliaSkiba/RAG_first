from pathlib import Path
from collections import Counter
import re


def load_markdown_previews(folder: Path) -> dict[str, str]:
    """Loads all the markdowns files in a given folder."""
    documents = {}

    for file in folder.glob("*.md"):
        with file.open('r', encoding="utf-8") as f:
            first_chars = f.read(100)
        documents[file.name] = first_chars
    return documents


def count_characters(text: str) -> Counter:
    """Returns the number of characters in the text."""

    return Counter(text)


def build_frequency_dictionary(counter: Counter) -> dict[str, int]:
    """Converts a counter into a frequency dictionary."""

    return dict(counter.most_common())


def build_word_frequency(text: str) -> Counter:
    """Counts how many times each word appears in the text."""

    words = re.findall(r"[A-Za-zÀ-ÿ]+", text.lower())
    return Counter(words)


def find_suspicious_tokens(text: str) -> list[str]:
    """Finds words containing ; or 8 between letters."""

    return re.findall(
        r"[A-Za-zÀ-ÿ'’\-]+[;8][A-Za-zÀ-ÿ'’\-]+",
        text
    )
