import re
from src.cleaning.replacements import OCR_REPLACEMENTS
from html import unescape


def replace_tabs(text: str) -> str:
    """Replaces tab characters with spaces."""
    return text.replace("\t", " ")


def remove_image_markers(text: str) -> str:
    """Removes image markers from the text."""
    return text.replace("<!-- image -->", "")


def normalize_spaces(text: str) -> str:
    """Normalizes repeated spaces."""
    return re.sub(r"\n{3,}", "\n\n", text)


def remove_trailing_spaces(text: str) -> str:
    """Removes spaces at the end of each line."""
    lines = text.splitlines()

    cleaned_lines = [
        line.rstrip()
        for line in lines
    ]

    return "\n".join(cleaned_lines)


def correct_known_ocr_errors(text: str) -> str:
    """Corrects known OCR errors while preserving capitalization."""
    incorrect_words = [
        word for word in OCR_REPLACEMENTS
        if word
    ]

    if not incorrect_words:
        return text

    pattern = re.compile(
        "|".join(re.escape(word) for word in incorrect_words),
        re.IGNORECASE,
    )


    def replace_match(match: re.Match) -> str:
        original_word = match.group(0)
        correct_word = OCR_REPLACEMENTS.get(original_word.lower())

        if correct_word is None:
            return original_word

        if original_word.isupper():
            return correct_word.upper()

        if original_word[0].isupper():
            return correct_word.capitalize()

        return correct_word

    return pattern.sub(replace_match, text)


def decode_html_entities(text: str) -> str:
    """Converts HTML entities to normal characters."""
    return unescape(text)


def clean_text(text: str) -> str:
    """Applies all cleaning rules to the text."""
    text = replace_tabs(text)
    text = remove_image_markers(text)
    text = decode_html_entities(text)
    text = normalize_spaces(text)
    text = remove_trailing_spaces(text)
    text = correct_known_ocr_errors(text)
    return text