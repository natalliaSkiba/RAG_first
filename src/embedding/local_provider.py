from sentence_transformers import SentenceTransformer

from src.embedding.config import EmbeddingModelConfig
from src.embedding.provider import EmbeddingProvider


class LocalSentenceTransformerProvider(EmbeddingProvider):
    """ Local embedding provider based on sentence-transformers."""

    def __init__(
        self,
        config: EmbeddingModelConfig,
    ) -> None:
        """ Loads the local embedding model."""

        super().__init__(config=config)

        self.model = SentenceTransformer(
            config.model_name,
        )

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """ Converts texts into real embedding vectors."""

        embeddings = self.model.encode(
            texts,
            batch_size=self.config.batch_size,
            normalize_embeddings=self.config.normalize_embeddings,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return [
            [
                float(value)
                for value in embedding.tolist()
            ]
            for embedding in embeddings
        ]