from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ChunkMetadata:
    """Stores information about the source and structure of a chunk."""

    source: str
    chunk_number: int
    heading: str
    heading_path: list[str] = field(default_factory=list)
    chunk_type: str = "text"
    images: list[str] = field(default_factory=list)
    section_id: str | None = None
    start_char: int | None = None
    end_char: int | None = None


@dataclass
class MarkdownBlock:
    """Represents one structural block extracted from a Markdown document. """

    block_type: str
    text: str
    heading_path: list[str] = field(default_factory=list)
    start_char: int | None = None
    end_char: int | None = None
    heading_level: int | None = None


@dataclass
class Section:
    """Represents one educational topic built from Markdown blocks. """

    section_id: str
    heading_path: list[str]
    blocks: list[MarkdownBlock] = field(default_factory=list)
    start_char: int | None = None
    end_char: int | None = None


@dataclass
class Chunk:
    """Represents one text chunk prepared for indexing."""

    chunk_id: str
    text: str
    metadata: ChunkMetadata

    def to_dict(self) -> dict[str, Any]:
        """Converts the chunk to a JSON-compatible dictionary."""

        metadata = asdict(self.metadata)
        metadata["size_chars"] = len(self.text)

        return {
            "id": self.chunk_id,
            "text": self.text,
            "metadata": metadata,
        }