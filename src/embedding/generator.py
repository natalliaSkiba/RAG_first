from src.embedding.models import (
    ChunkRecord,
    EmbeddingRecord,
    create_embedding_record,
)
from src.embedding.provider import EmbeddingProvider


def generate_embedding_records(
    chunks: list[ChunkRecord],
    provider: EmbeddingProvider,
) -> list[EmbeddingRecord]:
    """Generates embedding records for chunks."""

    texts = [
        chunk.get_embedding_text(
            config=provider.config,
        )
        for chunk in chunks
    ]

    embeddings = provider.embed_texts(texts)

    if len(embeddings) != len(chunks):
        raise ValueError(
            f"Expected {len(chunks)} embeddings, "
            f"got {len(embeddings)}"
        )

    records: list[EmbeddingRecord] = []

    for chunk, embedding in zip(chunks, embeddings):
        validate_embedding_dimension(
            embedding=embedding,
            expected_dimension=provider.config.dimension,
            chunk_id=chunk.chunk_id,
        )

        record = create_embedding_record(
            chunk=chunk,
            embedding=embedding,
            config=provider.config,
        )

        records.append(record)

    return records


def validate_embedding_dimension(
    embedding: list[float],
    expected_dimension: int,
    chunk_id: str,
) -> None:
    """ Validates embedding vector dimension."""

    if len(embedding) != expected_dimension:
        raise ValueError(
            f"Invalid embedding dimension for chunk {chunk_id}: "
            f"expected {expected_dimension}, got {len(embedding)}"
        )