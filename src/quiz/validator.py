from src.quiz.models import Quiz


def validate_quiz_sources(
    quiz: Quiz,
    source_texts: dict[str, str],
) -> None:
    """Validate chunk IDs and evidence against retrieved source texts."""

    if not source_texts:
        raise ValueError("Source texts must not be empty")

    for question_index, question in enumerate(quiz.questions, start=1):
        cited_texts: list[str] = []

        for chunk_id in question.source_chunk_ids:
            if chunk_id not in source_texts:
                raise ValueError(
                    f"Question {question_index} contains unknown "
                    f"source chunk ID: {chunk_id}"
                )

            cited_texts.append(source_texts[chunk_id])

        evidence_exists = any(
            question.evidence in source_text
            for source_text in cited_texts
        )

        if not evidence_exists:
            raise ValueError(
                f"Question {question_index} evidence was not found "
                "in the cited source chunks"
            )

        correct_option = question.options[
            question.correct_option_index
        ].strip()

        normalized_correct_option = correct_option.casefold().strip(" .")
        normalized_evidence = question.evidence.casefold()

        if normalized_correct_option not in normalized_evidence:
            raise ValueError(
                f"Question {question_index} correct option "
                "is not supported directly by evidence"
            )