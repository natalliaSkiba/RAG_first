from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.provider import DummyEmbeddingProvider


config = DEFAULT_EMBEDDING_CONFIG

provider = DummyEmbeddingProvider(
    config=config,
)

texts = [
    "passage: Ceci est un test.",
    "passage: Signalisation des trains.",
]

embeddings = provider.embed_texts(texts)

print("Embedding provider test")
print(f"Provider: {config.provider}")
print(f"Model: {config.model_name}")
print(f"Expected dimension: {config.dimension}")
print(f"Input texts: {len(texts)}")
print(f"Output vectors: {len(embeddings)}")
print()

for index, embedding in enumerate(embeddings, start=1):
    print(
        f"Vector {index}: "
        f"dimension={len(embedding)}, "
        f"first_values={embedding[:5]}"
    )

if len(embeddings) != len(texts):
    raise SystemExit(
        f"Expected {len(texts)} embeddings, got {len(embeddings)}"
    )

for embedding in embeddings:
    if len(embedding) != config.dimension:
        raise SystemExit(
            f"Expected dimension {config.dimension}, "
            f"got {len(embedding)}"
        )

print()
print("Embedding provider test completed.")