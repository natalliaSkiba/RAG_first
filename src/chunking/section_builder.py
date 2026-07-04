from src.chunking.models import MarkdownBlock, Section


def build_sections(
    blocks: list[MarkdownBlock],
) -> list[Section]:
    """ Groups Markdown blocks into educational sections."""

    # Stores all completed sections.
    sections: list[Section] = []

    # Stores blocks belonging to the current section.
    current_blocks: list[MarkdownBlock] = []

    # Stores the heading path of the current section.
    current_heading_path: list[str] | None = None

    for block in blocks:
        # Heading blocks are not added separately because their information is already stored in heading_path.
        if block.block_type == "heading":
            continue

        # The first content block starts the first section.
        if current_heading_path is None:
            current_heading_path = block.heading_path.copy()

        # A different heading path means that a new topic has started.
        if block.heading_path != current_heading_path:
            section_number = len(sections) + 1

            sections.append(
                Section(
                    section_id=f"section_{section_number:03d}",
                    heading_path=current_heading_path.copy(),
                    blocks=current_blocks.copy(),
                    start_char=current_blocks[0].start_char,
                    end_char=current_blocks[-1].end_char,
                )
            )

            # Start collecting blocks for the new section.
            current_blocks = []
            current_heading_path = block.heading_path.copy()

        # Add the current text or table block to the section.
        current_blocks.append(block)

    # Save the last section after processing all blocks.
    if current_blocks and current_heading_path is not None:
        section_number = len(sections) + 1

        sections.append(
            Section(
                section_id=f"section_{section_number:03d}",
                heading_path=current_heading_path.copy(),
                blocks=current_blocks.copy(),
                start_char=current_blocks[0].start_char,
                end_char=current_blocks[-1].end_char,
            )
        )

    return sections