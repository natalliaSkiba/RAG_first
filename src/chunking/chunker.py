from pathlib import Path

from src.chunking.models import (
    Chunk,
    ChunkMetadata,
    Section,
    TextPart,
)


MAX_CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150


def split_text_by_size(
    text: str,
    max_size: int = MAX_CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Splits long text into overlapping parts."""

    if max_size <= 0:
        raise ValueError("max_size must be greater than zero")

    if overlap < 0 or overlap >= max_size:
        raise ValueError(
            "overlap must be greater than or equal to zero "
            "and smaller than max_size"
        )

    cleaned_text = text.strip()

    if not cleaned_text:
        return []

    if len(cleaned_text) <= max_size:
        return [cleaned_text]

    chunks: list[str] = []
    start = 0

    while start < len(cleaned_text):
        end = min(
            start + max_size,
            len(cleaned_text),
        )

        if end < len(cleaned_text):
            # Search for a natural boundary in the second half.
            search_start = start + max_size // 2

            boundary = cleaned_text.rfind(
                "\n\n",
                search_start,
                end,
            )

            if boundary == -1:
                boundary = cleaned_text.rfind(
                    ". ",
                    search_start,
                    end,
                )

                if boundary != -1:
                    boundary += 1

            if boundary == -1:
                boundary = cleaned_text.rfind(
                    " ",
                    search_start,
                    end,
                )

            if boundary != -1:
                end = boundary

        chunk_text = cleaned_text[start:end].strip()

        if chunk_text:
            chunks.append(chunk_text)

        if end >= len(cleaned_text):
            break

        start = max(
            end - overlap,
            start + 1,
        )

    return chunks


def create_text_parts(section: Section) -> list[TextPart]:
    """Creates text parts while preserving image positions."""

    text_parts: list[TextPart] = []
    pending_images: list[str] = []
    part_number = 1

    for block in section.blocks:
        if block.block_type == "image":
            if block.image_path is None:
                continue

            # An image after text belongs to the latest text part.
            if text_parts:
                text_parts[-1].images.append(
                    block.image_path
                )
            else:
                # Images before the first text wait for that text.
                pending_images.append(
                    block.image_path
                )

            continue

        if block.block_type not in {"text", "table"}:
            continue

        if block.block_type == "table":
            # Preserve the complete Markdown table.
            split_parts = [block.text.strip()]
        else:
            split_parts = split_text_by_size(block.text)

        for split_index, part_text in enumerate(split_parts):
            part_images: list[str] = []

            # Attach leading images to the first part of the block.
            if split_index == 0 and pending_images:
                part_images = pending_images.copy()
                pending_images = []

            text_parts.append(
                TextPart(
                    text=part_text,
                    part_number=part_number,
                    images=part_images,
                    chunk_type=block.block_type,
                    start_char=block.start_char,
                    end_char=block.end_char,
                )
            )

            part_number += 1

    # Preserve sections containing only images.
    if not text_parts and pending_images:
        text_parts.append(
            TextPart(
                text="",
                part_number=1,
                images=pending_images.copy(),
                chunk_type="image",
                start_char=section.start_char,
                end_char=section.end_char,
            )
        )

    return text_parts


def build_section_text(section: Section) -> str:
    """Combines all text blocks of one section into a single text."""

    parts: list[str] = []

    for block in section.blocks:
        # Image blocks have no text and are stored separately.
        if not block.text.strip():
            continue

        parts.append(block.text.strip())

    return "\n\n".join(parts)


def get_section_images(section: Section) -> list[str]:
    """Returns image paths associated with a section."""

    images: list[str] = []

    for block in section.blocks:
        if (
            block.block_type == "image"
            and block.image_path is not None
        ):
            images.append(block.image_path)

    return images


def get_section_heading(
    section: Section,
    source: str,
) -> str:
    """Returns the section heading or the source filename."""

    if section.heading_path:
        return section.heading_path[-1]

    return Path(source).stem


def get_section_chunk_type(section: Section) -> str:
    """Determines the content type_of a section."""

    content_types = {
        block.block_type
        for block in section.blocks
        if block.block_type in {"text", "table"}
    }

    if content_types == {"table"}:
        return "table"

    if "table" in content_types:
        return "mixed"

    return "text"


def create_chunk_from_section(
    section: Section,
    source: str,
    chunk_number: int,
) -> Chunk:
    """Creates one chunk from one section."""

    section_text = build_section_text(section)

    chunk_id = (
        f"{Path(source).stem}_"
        f"chunk_{chunk_number:04d}"
    )

    metadata = ChunkMetadata(
        source=source,
        chunk_number=chunk_number,
        heading=get_section_heading(
            section=section,
            source=source,
        ),
        heading_path=section.heading_path.copy(),
        chunk_type=get_section_chunk_type(section),
        images=get_section_images(section),
        section_id=section.section_id,
        start_char=section.start_char,
        end_char=section.end_char,
    )

    return Chunk(
        chunk_id=chunk_id,
        text=section_text,
        metadata=metadata,
    )


def create_chunk_from_text_part(
    section: Section,
    text_part: TextPart,
    source: str,
    chunk_number: int,
) -> Chunk:
    """Creates one chunk from one text part."""

    chunk_id = (
        f"{Path(source).stem}_"
        f"chunk_{chunk_number:04d}"
    )

    chunk_text = text_part.text

    if not chunk_text.strip() and text_part.images:
        chunk_text = get_section_heading(
            section=section,
            source=source,
        )

    metadata = ChunkMetadata(
        source=source,
        chunk_number=chunk_number,
        heading=get_section_heading(
            section=section,
            source=source,
        ),
        heading_path=section.heading_path.copy(),
        chunk_type=text_part.chunk_type,
        images=text_part.images.copy(),
        section_id=section.section_id,
        start_char=text_part.start_char,
        end_char=text_part.end_char,
    )

    return Chunk(
        chunk_id=chunk_id,
        text=chunk_text,
        metadata=metadata,
    )


def create_chunks_from_section(
    section: Section,
    source: str,
    start_chunk_number: int,
) -> list[Chunk]:
    """Creates all chunks for one section."""

    text_parts = create_text_parts(section)
    chunks: list[Chunk] = []

    for offset, text_part in enumerate(text_parts):
        chunk_number = start_chunk_number + offset

        chunk = create_chunk_from_text_part(
            section=section,
            text_part=text_part,
            source=source,
            chunk_number=chunk_number,
        )

        chunks.append(chunk)

    return chunks


def create_chunks(
    sections: list[Section],
    source: str,
) -> list[Chunk]:
    """
    Creates chunks for all sections of one document.

    Создаёт chunks для всех секций одного документа.
    """

    chunks: list[Chunk] = []
    next_chunk_number = 1

    for section in sections:
        section_chunks = create_chunks_from_section(
            section=section,
            source=source,
            start_chunk_number=next_chunk_number,
        )

        chunks.extend(section_chunks)

        next_chunk_number += len(section_chunks)

    return chunks