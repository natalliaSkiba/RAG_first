from src.retrieval.models import HybridSearchResult


def build_quiz_context(
    results: list[HybridSearchResult],
) -> str:
    """Builds a structured source context for quiz generation."""

    if not results:
        raise ValueError("Search results must not be empty")

    context_parts: list[str] = []

    for result in results:
        record = result.record
        heading = str(record.metadata.get("heading", "")).strip()

        context_part = (
            f"CHUNK_ID: {record.chunk_id}\n"
            f"HEADING: {heading}\n"
            f"CONTENT:\n{record.text.strip()}"
        )

        context_parts.append(context_part)

    return "\n\n---\n\n".join(context_parts)