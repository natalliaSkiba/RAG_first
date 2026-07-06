from dataclasses import dataclass, field
from typing import Any

from src.embedding.config import EmbeddingModelConfig


@dataclass
class ChunkRecord:
    """Represents one chunk loaded from data/chunks/*.jsonl."""

    chunk_id: str
    text: str
    metadata: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChunkRecord":
        """Creates a ChunkRecord from a _JSONL dictionary."""

        return cls(
            chunk_id=str(data["id"]),
            text=str(data["text"]),
            metadata=dict(data["metadata"]),
        )

    def get_embedding_text(
        self,
        config: EmbeddingModelConfig,
    ) -> str:
        """Returns text prepared for passage embedding."""

        return f"{config.passage_prefix}{self.text}"


@dataclass
class EmbeddingRecord:
    """ Represents the future JSONL output structure for embeddings."""

    chunk_id: str
    text: str
    metadata: dict[str, Any]
    embedding: list[float] = field(default_factory=list)
    embedding_metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Converts the embedding record to a JSON-compatible dictionary."""

        return {
            "id": self.chunk_id,
            "text": self.text,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "embedding_metadata": self.embedding_metadata,
        }


def create_empty_embedding_record(
    chunk: ChunkRecord,
    config: EmbeddingModelConfig,
) -> EmbeddingRecord:
    """ Creates the output structure before real vector generation."""

    return EmbeddingRecord(
        chunk_id=chunk.chunk_id,
        text=chunk.text,
        metadata=chunk.metadata.copy(),
        embedding=[],
        embedding_metadata={
            "provider": config.provider,
            "model_name": config.model_name,
            "dimension": config.dimension,
            "text_prefix": config.passage_prefix,
            "normalize_embeddings": config.normalize_embeddings,
        },
    )