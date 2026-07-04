import re

from src.chunking.models import MarkdownBlock


# Matches Markdown headings from level 1 to level 6.
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

# Matches one separator cell of a Markdown table.
TABLE_SEPARATOR_CELL_PATTERN = re.compile(r"^:?-{3,}:?$")


def parse_heading(line: str) -> tuple[int, str] | None:
    """Extracts the level and text of a Markdown heading."""

    match = HEADING_PATTERN.match(line)

    if match is None:
        return None

    heading_level = len(match.group(1))
    heading_text = match.group(2).strip()

    return heading_level, heading_text


def is_table_separator(line: str) -> bool:
    """ Checks whether a line is a Markdown table separator."""

    stripped_line = line.strip().strip("|")

    if not stripped_line:
        return False

    cells = [cell.strip() for cell in stripped_line.split("|")]

    return (
        len(cells) >= 2
        and all(
            TABLE_SEPARATOR_CELL_PATTERN.fullmatch(cell) is not None
            for cell in cells
        )
    )


def is_table_row(line: str) -> bool:
    """Checks whether a line can be a Markdown table row."""

    stripped_line = line.strip()

    if not stripped_line or "|" not in stripped_line:
        return False

    cells = [
        cell.strip()
        for cell in stripped_line.strip("|").split("|")
    ]

    return len(cells) >= 2


def is_table_start(current_line: str, next_line: str) -> bool:
    """
    Checks whether two lines start a Markdown table."""

    return (
        is_table_row(current_line)
        and is_table_separator(next_line)
    )


def _split_lines_with_positions(
    markdown_text: str,
) -> list[tuple[str, int, int]]:
    """Splits Markdown text into lines and stores their positions."""

    lines_with_positions: list[tuple[str, int, int]] = []
    current_position = 0

    # keepends=True keeps newline characters in raw_line.
    for raw_line in markdown_text.splitlines(keepends=True):
        # Remove only newline characters from the line.
        line = raw_line.rstrip("\r\n")

        start_char = current_position
        end_char = start_char + len(line)

        lines_with_positions.append(
            (line, start_char, end_char)
        )

        # Move the position by the full raw line length, including newline characters.
        current_position += len(raw_line)

    return lines_with_positions


def _get_heading_path(
    headings: list[tuple[int, str]],
) -> list[str]:
    """Returns only heading texts without their levels."""

    return [
        heading_text
        for _, heading_text in headings
    ]


def _create_text_block(
    text_lines: list[tuple[str, int, int]],
    heading_path: list[str],
) -> MarkdownBlock | None:
    """Creates one text block from accumulated lines."""

    if not text_lines:
        return None

    start_index = 0
    end_index = len(text_lines)

    # Remove empty lines from the beginning.
    while (
        start_index < end_index
        and not text_lines[start_index][0].strip()
    ):
        start_index += 1

    # Remove empty lines from the end.
    while (
        end_index > start_index
        and not text_lines[end_index - 1][0].strip()
    ):
        end_index -= 1

    trimmed_lines = text_lines[start_index:end_index]

    if not trimmed_lines:
        return None

    text = "\n".join(
        line
        for line, _, _ in trimmed_lines
    )

    start_char = trimmed_lines[0][1]
    end_char = trimmed_lines[-1][2]

    return MarkdownBlock(
        block_type="text",
        text=text,
        heading_path=heading_path.copy(),
        start_char=start_char,
        end_char=end_char,
    )


def parse_markdown(markdown_text: str) -> list[MarkdownBlock]:
    """Splits a Markdown document into heading, text and table blocks."""

    blocks: list[MarkdownBlock] = []

    # Headings currently associated with document content.
    active_headings: list[tuple[int, str]] = []

    # Headings found one after another before the next content block.
    pending_headings: list[tuple[int, str]] = []

    # Ordinary text lines waiting to become one text block.
    text_buffer: list[tuple[str, int, int]] = []

    lines = _split_lines_with_positions(markdown_text)

    index = 0

    while index < len(lines):
        line, start_char, end_char = lines[index]

        heading = parse_heading(line)

        if heading is not None:
            # Save ordinary text collected before this heading.
            text_block = _create_text_block(
                text_buffer,
                _get_heading_path(active_headings),
            )

            if text_block is not None:
                blocks.append(text_block)

            text_buffer = []

            heading_level, heading_text = heading

            if pending_headings:
                # Several headings in a row belong to one topic path.
                pending_headings.append(
                    (heading_level, heading_text)
                )
            else:
                # Keep only real parent headings.
                parent_headings = [
                    active_heading
                    for active_heading in active_headings
                    if active_heading[0] < heading_level
                ]

                pending_headings = parent_headings + [
                    (heading_level, heading_text)
                ]

            blocks.append(
                MarkdownBlock(
                    block_type="heading",
                    text=heading_text,
                    heading_path=_get_heading_path(
                        pending_headings
                    ),
                    start_char=start_char,
                    end_char=end_char,
                    heading_level=heading_level,
                )
            )

            index += 1
            continue

        # Ignore empty lines between consecutive headings.
        if not line.strip():
            if text_buffer:
                text_buffer.append(
                    (line, start_char, end_char)
                )

            index += 1
            continue

        # The first real content after headings activates their path.
        if pending_headings:
            active_headings = pending_headings.copy()
            pending_headings = []

        next_line = ""

        if index + 1 < len(lines):
            next_line = lines[index + 1][0]

        if is_table_start(line, next_line):
            # Save ordinary text collected before the table.
            text_block = _create_text_block(
                text_buffer,
                _get_heading_path(active_headings),
            )

            if text_block is not None:
                blocks.append(text_block)

            text_buffer = []

            table_lines: list[tuple[str, int, int]] = []

            # Add the table header.
            table_lines.append(lines[index])
            index += 1

            # Add the table separator.
            table_lines.append(lines[index])
            index += 1

            # Add all following table rows.
            while (
                index < len(lines)
                and is_table_row(lines[index][0])
            ):
                table_lines.append(lines[index])
                index += 1

            table_text = "\n".join(
                table_line
                for table_line, _, _ in table_lines
            )

            blocks.append(
                MarkdownBlock(
                    block_type="table",
                    text=table_text,
                    heading_path=_get_heading_path(
                        active_headings
                    ),
                    start_char=table_lines[0][1],
                    end_char=table_lines[-1][2],
                )
            )

            continue

        # The line is ordinary text.
        text_buffer.append(
            (line, start_char, end_char)
        )

        index += 1

    # Save ordinary text remaining at the end of the document.
    final_text_block = _create_text_block(
        text_buffer,
        _get_heading_path(active_headings),
    )

    if final_text_block is not None:
        blocks.append(final_text_block)

    return blocks