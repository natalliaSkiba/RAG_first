import re
import unicodedata

from src.retrieval.models import (
    HybridSearchResult,
    RetrievalRecord,
    SearchResult,
)


FRENCH_STOPWORDS = {
    "que",
    "quoi",
    "faire",
    "cas",
    "en",
    "de",
    "du",
    "des",
    "la",
    "le",
    "les",
    "un",
    "une",
    "et",
    "ou",
    "a",
    "au",
    "aux",
    "pour",
    "par",
    "sur",
    "dans",
    "avec",
}


DOMAIN_QUERY_EXPANSIONS = {
    "detresse": [
        "detresse",
        "dsec",
        "secours",
        "degagement",
    ],
    "secours": [
        "secours",
        "dsec",
        "detresse",
        "degagement",
    ],
    "dsec": [
        "dsec",
        "detresse",
        "secours",
    ],
}


def normalize_text(text: str) -> str:
    """Normalizes text for keyword matching.
    Example:
    "DÉTRESSE" -> "detresse" """

    decomposed_text = unicodedata.normalize(
        "NFKD",
        text,
    )

    text_without_accents = "".join(
        character
        for character in decomposed_text
        if not unicodedata.combining(character)
    )

    return text_without_accents.lower()


def extract_query_terms(question: str) -> list[str]:
    """ Extracts useful keywords from a user question."""

    normalized_question = normalize_text(question)

    raw_terms = re.findall(
        r"[a-z0-9]+",
        normalized_question,
    )

    terms = [
        term
        for term in raw_terms
        if term not in FRENCH_STOPWORDS and len(term) >= 3
    ]

    return terms


def expand_query_terms(terms: list[str]) -> list[str]:
    """ Adds domain-specific related terms. """

    expanded_terms: list[str] = []

    for term in terms:
        expanded_terms.append(term)

        related_terms = DOMAIN_QUERY_EXPANSIONS.get(
            term,
            [],
        )

        expanded_terms.extend(related_terms)

    unique_terms = sorted(set(expanded_terms))

    return unique_terms


def dot_product(
    left_vector: list[float],
    right_vector: list[float],
) -> float:
    """  Calculates dot product similarity between two vectors.
    Important:
    If vectors are normalized, dot product works like cosine similarity. """

    if len(left_vector) != len(right_vector):
        raise ValueError(
            "Vector dimensions are different: "
            f"{len(left_vector)} != {len(right_vector)}"
        )

    return sum(
        left_value * right_value
        for left_value, right_value in zip(left_vector, right_vector)
    )


def calculate_keyword_score(
    question: str,
    record: RetrievalRecord,
) -> float:
    """ Calculates a small keyword boost for technical terms."""

    query_terms = extract_query_terms(
        question=question,
    )

    expanded_terms = expand_query_terms(
        terms=query_terms,
    )

    if not expanded_terms:
        return 0.0

    heading = normalize_text(
        str(
            record.metadata.get(
                "heading",
                "",
            )
        )
    )

    text = normalize_text(record.text)

    keyword_score = 0.0

    for term in expanded_terms:
        if term in heading:
            keyword_score += 0.07

        if term in text:
            keyword_score += 0.03

    max_keyword_score = 0.25

    return min(
        keyword_score,
        max_keyword_score,
    )


def search_by_vector(
    query_embedding: list[float],
    records: list[RetrievalRecord],
    top_k: int = 5,
) -> list[SearchResult]:
    """Searches the most similar records for a query embedding."""

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    scored_results: list[tuple[float, RetrievalRecord]] = []

    for record in records:
        score = dot_product(
            query_embedding,
            record.embedding,
        )

        scored_results.append(
            (
                score,
                record,
            )
        )

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    top_results = scored_results[:top_k]

    return [
        SearchResult(
            rank=rank,
            score=score,
            record=record,
        )
        for rank, (score, record) in enumerate(
            top_results,
            start=1,
        )
    ]


def search_by_vector_hybrid(
    question: str,
    query_embedding: list[float],
    records: list[RetrievalRecord],
    top_k: int = 5,
) -> list[HybridSearchResult]:
    """Searches records using semantic score plus keyword boost."""

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    scored_results: list[tuple[float, float, float, RetrievalRecord]] = []

    for record in records:
        semantic_score = dot_product(
            query_embedding,
            record.embedding,
        )

        keyword_score = calculate_keyword_score(
            question=question,
            record=record,
        )

        final_score = semantic_score + keyword_score

        scored_results.append(
            (
                final_score,
                semantic_score,
                keyword_score,
                record,
            )
        )

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    top_results = scored_results[:top_k]

    return [
        HybridSearchResult(
            rank=rank,
            score=final_score,
            semantic_score=semantic_score,
            keyword_score=keyword_score,
            record=record,
        )
        for rank, (
            final_score,
            semantic_score,
            keyword_score,
            record,
        ) in enumerate(
            top_results,
            start=1,
        )
    ]