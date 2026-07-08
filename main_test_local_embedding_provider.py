from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.embedding.local_provider import LocalSentenceTransformerProvider


config = DEFAULT_EMBEDDING_CONFIG

provider = LocalSentenceTransformerProvider(
    config=config,
)

texts = [
    "passage: Signalisation des trains.",
    "passage: Risques ferroviaires et communication.",
]

embeddings = provider.embed_texts(texts)

print("Local embedding provider test")
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

    if all(value == 0.0 for value in embedding):
        raise SystemExit(
            "Embedding vector contains only zeros"
        )

print()
print("Local embedding provider test completed.")