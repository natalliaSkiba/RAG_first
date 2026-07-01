import re

def fix_systematic_ocr_errors(text: str) -> str:
    """
    Fixes known systematic OCR errors.
    """
    # Fix: ti -> ;
    text = re.sub(r'([a-zA-Z]);([a-zA-Z])', r'\1ti\2', text)

    # Fix: ti -> 8
    text = re.sub(r'([a-zA-Z])8([a-zA-Z])', r'\1ti\2', text)

    # Fix: tt -> F
    text = re.sub(r'([a-z])F([a-z])', r'\1tt\2', text)

    return text

def remove_structural_junk(text: str) -> str:
    """
    Removes markup junk and normalizes spaces.
    """
    #  Remove empty image tags
    text = text.replace('', '')

    # Replace tabs with spaces
    text = text.replace('\t', ' ')

    # Replace multiple spaces with one
    text = re.sub(r' +', ' ', text)

    # Remove multiple empty lines (replace 3 or more with 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()