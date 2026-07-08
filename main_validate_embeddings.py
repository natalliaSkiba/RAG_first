from pathlib import Path

from src.embedding.config import DEFAULT_EMBEDDING_CONFIG
from src.validation.validate_embeddings import validate_embedding_folder


input_folder = Path("data/embeddings")
expected_total_records = 455

config = DEFAULT_EMBEDDING_CONFIG

errors = validate_embedding_folder(
    input_folder=input_folder,
    expected_total_records=expected_total_records,
    expected_dimension=config.dimension,
    allow_empty_embeddings=False,
)

print("Embedding validation")
print(f"Input folder: {input_folder}")
print(f"Expected records: {expected_total_records}")
print(f"Expected dimension: {config.dimension}")
#print(f"Allow empty embeddings: True")
print(f"Allow empty embeddings: False")
print()

if errors:
    print("Validation errors:")
    for error in errors:
        print(f"- {error}")

    raise SystemExit(
        f"Embedding validation failed: {len(errors)} errors"
    )

print("Validation errors: 0")
print("Embedding validation completed.")