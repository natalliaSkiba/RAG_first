from src.embedding.config import EmbeddingModelConfig
from src.embedding.provider import EmbeddingProvider


def prepare_query_text(
    question: str,
    config: EmbeddingModelConfig,
) -> str:
    """Prepares user question for query embedding."""

    clean_question = question.strip()

    if not clean_question:
        raise ValueError("Question must not be empty")

    return f"{config.query_prefix}{clean_question}"


def generate_query_embedding(
    question: str,
    provider: EmbeddingProvider,
) -> list[float]:
    """ Generates one embedding vector for a user question."""

    query_text = prepare_query_text(
        question=question,
        config=provider.config,
    )

    embeddings = provider.embed_texts(
        texts=[query_text],
    )

    if len(embeddings) != 1:
        raise ValueError(
            f"Expected 1 query embedding, got {len(embeddings)}"
        )

    query_embedding = embeddings[0]

    if len(query_embedding) != provider.config.dimension:
        raise ValueError(
            "Invalid query embedding dimension: "
            f"expected {provider.config.dimension}, "
            f"got {len(query_embedding)}"
        )

    return query_embedding