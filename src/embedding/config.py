from dataclasses import dataclass


@dataclass(frozen=True)
class EmbeddingModelConfig:
    """Stores embedding model configuration."""

    provider: str
    model_name: str
    dimension: int
    passage_prefix: str
    query_prefix: str
    normalize_embeddings: bool
    batch_size: int

    def get_prefix(self, text_type: str) -> str:
        """Returns the correct prefix for passage or query text."""

        if text_type == "passage":
            return self.passage_prefix

        if text_type == "query":
            return self.query_prefix

        raise ValueError(
            f"Unsupported text type: {text_type}. "
            "Expected 'passage' or 'query'."
        )


DEFAULT_EMBEDDING_CONFIG = EmbeddingModelConfig(
    provider="local",
    model_name="intfloat/multilingual-e5-small",
    dimension=384,
    passage_prefix="passage: ",
    query_prefix="query: ",
    normalize_embeddings=True,
    batch_size=32,
)