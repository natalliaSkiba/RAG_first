import json
from pathlib import Path

from src.embedding.models import ChunkRecord


def read_chunks_from_jsonl(file_path: Path) -> list[ChunkRecord]:
    """Reads one _JSONL_ chunk file."""

    chunks: list[ChunkRecord] = []

    with file_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                chunk = ChunkRecord.from_dict(data)
            except (json.JSONDecodeError, KeyError, TypeError) as error:
                raise ValueError(
                    f"Invalid chunk JSONL record in {file_path} "
                    f"at line {line_number}: {error}"
                ) from error

            chunks.append(chunk)

    return chunks


def read_chunks_from_folder(input_folder: Path) -> list[ChunkRecord]:
    """Reads all _JSONL_ chunk files from a folder."""

    all_chunks: list[ChunkRecord] = []

    for file_path in sorted(input_folder.glob("*.jsonl")):
        file_chunks = read_chunks_from_jsonl(file_path)
        all_chunks.extend(file_chunks)

    return all_chunks


def count_chunks_by_file(input_folder: Path) -> dict[str, int]:
    """ Counts chunks in each _JSONL_ file."""

    counts: dict[str, int] = {}

    for file_path in sorted(input_folder.glob("*.jsonl")):
        counts[file_path.name] = len(
            read_chunks_from_jsonl(file_path)
        )

    return counts