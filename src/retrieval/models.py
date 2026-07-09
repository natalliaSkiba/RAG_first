from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RetrievalRecord:
    """Represents one embedded chunk loaded from data/embeddings/*.jsonl."""

    chunk_id: str
    text: str
    embedding: list[float]
    metadata: dict[str, Any]
    embedding_metadata: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RetrievalRecord":
        """Creates a RetrievalRecord from a JSONL dictionary."""

        return cls(
            chunk_id=str(data["id"]),
            text=str(data["text"]),
            embedding=list(data["embedding"]),
            metadata=dict(data["metadata"]),
            embedding_metadata=dict(data["embedding_metadata"]),
        )

    def get_images(self) -> list[str]:
        """Returns image paths linked to this chunk."""

        images = self.metadata.get("images", [])

        if not isinstance(images, list):
            return []

        return [str(image) for image in images]


@dataclass(frozen=True)
class SearchResult:
    """Represents one semantic search result."""

    rank: int
    score: float
    record: RetrievalRecord

@dataclass(frozen=True)
class HybridSearchResult:
    """ Represents one hybrid search result."""

    rank: int
    score: float
    semantic_score: float
    keyword_score: float
    record: RetrievalRecord