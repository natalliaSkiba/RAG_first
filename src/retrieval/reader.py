import json
from pathlib import Path

from src.retrieval.models import RetrievalRecord


def read_embedding_records_from_jsonl(
    file_path: Path,
) -> list[RetrievalRecord]:
    """Reads one embedding JSONL file."""

    records: list[RetrievalRecord] = []

    with file_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                record = RetrievalRecord.from_dict(data)
            except (json.JSONDecodeError, KeyError, TypeError) as error:
                raise ValueError(
                    f"Invalid embedding JSONL record in {file_path} "
                    f"at line {line_number}: {error}"
                ) from error

            records.append(record)

    return records


def read_embedding_records_from_folder(
    input_folder: Path,
) -> list[RetrievalRecord]:
    """ Reads all embedding JSONL files from a folder."""

    all_records: list[RetrievalRecord] = []
    files = sorted(input_folder.glob("*_embeddings.jsonl"))

    if not files:
        raise FileNotFoundError(
            f"No embedding files found in {input_folder}"
        )

    for file_path in files:
        file_records = read_embedding_records_from_jsonl(file_path)
        all_records.extend(file_records)

    return all_records


def count_embedding_records_by_file(
    input_folder: Path,
) -> dict[str, int]:
    """Counts embedding records in each _JSONL_ file."""

    counts: dict[str, int] = {}

    for file_path in sorted(input_folder.glob("*_embeddings.jsonl")):
        counts[file_path.name] = len(
            read_embedding_records_from_jsonl(file_path)
        )

    return counts