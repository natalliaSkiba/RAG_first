from src.chunking.models import MarkdownBlock


def build_section_text(
    section: list[MarkdownBlock],
) -> str:
    """Combines all blocks of one section into a single text."""

    # Stores the text of each block.
    parts: list[str] = []

    for block in section:
        # Ignore empty blocks.
        if not block.text.strip():
            continue

        # Add the block text without extra spaces at the beginning and end.
        parts.append(block.text.strip())

    # Separate text blocks and tables with an empty line.
    return "\n\n".join(parts)