import json
from pathlib import Path

from src.chunking.models import Chunk


def write_chunks_to_jsonl(
    chunks: list[Chunk],
    output_file: Path,
) -> None:
    """Writes chunks to a JSONL file."""

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        for chunk in chunks:
            json_line = json.dumps(
                chunk.to_dict(),
                ensure_ascii=False,
            )

            file.write(json_line + "\n")