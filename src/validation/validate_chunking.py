from pathlib import Path

from src.chunking.models import Chunk
from src.chunking.chunker import MAX_CHUNK_SIZE


def validate_chunk(chunk: Chunk) -> list[str]:
    """Validates one chunk. """

    errors: list[str] = []

    if not chunk.chunk_id.strip():
        errors.append("Chunk ID is empty")

    if not chunk.text.strip():
        errors.append(
            f"{chunk.chunk_id}: chunk text is empty"
        )

    if not chunk.metadata.source.strip():
        errors.append(
            f"{chunk.chunk_id}: source is empty"
        )

    if chunk.metadata.chunk_number <= 0:
        errors.append(
            f"{chunk.chunk_id}: invalid chunk number"
        )

    if not chunk.metadata.heading.strip():
        errors.append(
            f"{chunk.chunk_id}: heading is empty"
        )

    if (
        len(chunk.text) > MAX_CHUNK_SIZE
        and chunk.metadata.chunk_type != "table"
    ):
        errors.append(
            f"{chunk.chunk_id}: text is too long "
            f"({len(chunk.text)} characters)"
        )

    for image_path in chunk.metadata.images:
        if not Path(image_path).exists():
            errors.append(
                f"{chunk.chunk_id}: image file does not exist: "
                f"{image_path}"
            )

    return errors


def validate_chunks(chunks: list[Chunk]) -> list[str]:
    """Validates a list of chunks."""

    errors: list[str] = []

    seen_chunk_ids: set[str] = set()
    expected_chunk_number = 1

    for chunk in chunks:
        errors.extend(validate_chunk(chunk))

        if chunk.chunk_id in seen_chunk_ids:
            errors.append(
                f"{chunk.chunk_id}: duplicate chunk ID"
            )

        seen_chunk_ids.add(chunk.chunk_id)

        if chunk.metadata.chunk_number != expected_chunk_number:
            errors.append(
                f"{chunk.chunk_id}: expected chunk number "
                f"{expected_chunk_number}, got "
                f"{chunk.metadata.chunk_number}"
            )

        expected_chunk_number += 1

    return errors