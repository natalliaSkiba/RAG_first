from abc import ABC, abstractmethod

from src.embedding.config import EmbeddingModelConfig


class EmbeddingProvider(ABC):
    """Base interface for all embedding providers."""

    def __init__(
        self,
        config: EmbeddingModelConfig,
    ) -> None:
        """ Stores embedding model configuration. """

        self.config = config

    @abstractmethod
    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Converts texts into embedding vectors."""

        raise NotImplementedError


class DummyEmbeddingProvider(EmbeddingProvider):
    """Temporary provider for testing the embedding pipeline."""

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Returns zero vectors with the configured dimension."""

        return [
            [0.0 for _ in range(self.config.dimension)]
            for _ in texts
        ]