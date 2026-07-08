import json
import math
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "id",
    "text",
    "embedding",
    "metadata",
    "embedding_metadata",
}

REQUIRED_EMBEDDING_METADATA_FIELDS = {
    "provider",
    "model_name",
    "dimension",
    "text_prefix",
    "normalize_embeddings",
}


def read_jsonl(file_path: Path) -> list[dict[str, Any]]:
    """Reads a _JSONL_ file and returns a list of dictionaries."""

    records: list[dict[str, Any]] = []

    with file_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON in {file_path} "
                    f"at line {line_number}: {error}"
                ) from error

            records.append(record)

    return records


def validate_embedding_record(
    record: dict[str, Any],
    file_path: Path,
    line_number: int,
    expected_dimension: int,
    allow_empty_embeddings: bool,
) -> list[str]:
    """Validates one embedding record."""

    errors: list[str] = []

    missing_fields = REQUIRED_FIELDS - record.keys()

    if missing_fields:
        errors.append(
            f"{file_path.name}:{line_number} "
            f"missing fields: {sorted(missing_fields)}"
        )
        return errors

    if not isinstance(record["id"], str) or not record["id"].strip():
        errors.append(
            f"{file_path.name}:{line_number} invalid id"
        )

    if not isinstance(record["text"], str) or not record["text"].strip():
        errors.append(
            f"{file_path.name}:{line_number} empty text"
        )

    if not isinstance(record["metadata"], dict):
        errors.append(
            f"{file_path.name}:{line_number} metadata must be dict"
        )

    if not isinstance(record["embedding_metadata"], dict):
        errors.append(
            f"{file_path.name}:{line_number} "
            "embedding_metadata must be dict"
        )
        return errors

    missing_embedding_metadata = (
        REQUIRED_EMBEDDING_METADATA_FIELDS
        - record["embedding_metadata"].keys()
    )

    if missing_embedding_metadata:
        errors.append(
            f"{file_path.name}:{line_number} "
            f"missing embedding_metadata fields: "
            f"{sorted(missing_embedding_metadata)}"
        )

    dimension = record["embedding_metadata"].get("dimension")

    if dimension != expected_dimension:
        errors.append(
            f"{file_path.name}:{line_number} "
            f"invalid dimension: {dimension}, "
            f"expected {expected_dimension}"
        )

    embedding = record["embedding"]

    if not isinstance(embedding, list):
        errors.append(
            f"{file_path.name}:{line_number} embedding must be list"
        )
        return errors

    if allow_empty_embeddings and len(embedding) == 0:
        return errors

    if len(embedding) != expected_dimension:
        errors.append(
            f"{file_path.name}:{line_number} "
            f"embedding length is {len(embedding)}, "
            f"expected {expected_dimension}"
        )

    all_values_are_float = True

    for index, value in enumerate(embedding):
        if not isinstance(value, float):
            errors.append(
                f"{file_path.name}:{line_number} "
                f"embedding[{index}] is not float"
            )
            all_values_are_float = False
            break

    if not all_values_are_float:
        return errors

    if embedding and all(value == 0.0 for value in embedding):
        errors.append(
            f"{file_path.name}:{line_number} "
            "embedding contains only zeros"
        )

    if embedding:
        vector_norm = math.sqrt(
            sum(value * value for value in embedding)
        )

        if not 0.99 <= vector_norm <= 1.01:
            errors.append(
                f"{file_path.name}:{line_number} "
                f"embedding norm is {vector_norm:.6f}, "
                "expected approximately 1.0"
            )

    return errors


def validate_embedding_folder(
    input_folder: Path,
    expected_total_records: int,
    expected_dimension: int,
    allow_empty_embeddings: bool = True,
) -> list[str]:
    """Validates all embedding _JSONL_ files in a folder."""

    errors: list[str] = []
    seen_ids: set[str] = set()
    total_records = 0

    files = sorted(input_folder.glob("*_embeddings.jsonl"))

    if not files:
        errors.append(
            f"No embedding files found in {input_folder}"
        )
        return errors

    for file_path in files:
        records = read_jsonl(file_path)

        if not records:
            errors.append(
                f"{file_path.name} is empty"
            )

        for line_number, record in enumerate(records, start=1):
            record_errors = validate_embedding_record(
                record=record,
                file_path=file_path,
                line_number=line_number,
                expected_dimension=expected_dimension,
                allow_empty_embeddings=allow_empty_embeddings,
            )
            errors.extend(record_errors)

            record_id = record.get("id")

            if isinstance(record_id, str):
                if record_id in seen_ids:
                    errors.append(
                        f"Duplicate embedding id: {record_id}"
                    )
                seen_ids.add(record_id)

        total_records += len(records)

    if total_records != expected_total_records:
        errors.append(
            f"Expected {expected_total_records} embedding records, "
            f"got {total_records}"
        )

    return errors
