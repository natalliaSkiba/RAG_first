import json
from pathlib import Path

from src.embedding.config import EmbeddingModelConfig
from src.embedding.models import (
    ChunkRecord,
    EmbeddingRecord,
    create_empty_embedding_record,
)


def write_embedding_records_to_jsonl(
    records: list[EmbeddingRecord],
    output_file: Path,
) -> None:
    """Writes embedding records to a JSONL file.

    Записывает embedding records в JSONL-файл.
    """

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        for record in records:
            file.write(
                json.dumps(
                    record.to_dict(),
                    ensure_ascii=False,
                )
            )
            file.write("\n")


def create_empty_embedding_records(
    chunks: list[ChunkRecord],
    config: EmbeddingModelConfig,
) -> list[EmbeddingRecord]:
    """
    Creates empty embedding records from chunks.

    Создаёт пустые embedding records из chunks.
    """

    return [
        create_empty_embedding_record(
            chunk=chunk,
            config=config,
        )
        for chunk in chunks
    ]


def build_embedding_output_file(
    input_file: Path,
    output_folder: Path,
) -> Path:
    """
    Builds output file path for embeddings.

    Создаёт путь output-файла для embeddings.
    """

    output_file_name = f"{input_file.stem}_embeddings.jsonl"

    return output_folder / output_file_name