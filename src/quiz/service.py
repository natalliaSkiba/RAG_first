from typing import Protocol

from src.quiz.context import build_quiz_context
from src.quiz.models import Quiz
from src.quiz.parser import parse_quiz_response
from src.quiz.prompt import build_quiz_prompt
from src.quiz.validator import validate_quiz_sources
from src.retrieval.models import HybridSearchResult


class QuizGenerator(Protocol):
    """Interface for quiz generators."""

    def generate(self, prompt: str) -> str:
        """Generate a quiz response from a prompt."""


def generate_quiz(
    generator: QuizGenerator,
    topic: str,
    search_results: list[HybridSearchResult],
    question_count: int = 10,
    max_attempts: int = 3,
) -> Quiz:
    """Generate and validate a quiz from retrieved chunks."""

    if max_attempts < 1:
        raise ValueError("Max attempts must be greater than zero")

    context = build_quiz_context(search_results)

    original_prompt = build_quiz_prompt(
        topic=topic,
        context=context,
        question_count=question_count,
    )

    source_texts = {
        result.record.chunk_id: result.record.text
        for result in search_results
    }

    current_prompt = original_prompt
    last_error: ValueError | None = None

    for attempt in range(1, max_attempts + 1):
        response_text = generator.generate(current_prompt)
        #print("\n--- RAW QUIZ RESPONSE ---")
        #print(response_text)
        #print("--- END RAW QUIZ RESPONSE ---\n")

        try:
            quiz = parse_quiz_response(response_text)

            validate_quiz_sources(
                quiz=quiz,
                source_texts=source_texts,
            )

            return quiz

        except ValueError as error:
            last_error = error

            current_prompt = (
                f"{original_prompt}\n\n"
                "The previous response was rejected.\n"
                f"Reason: {error}\n"
                "Generate the quiz again and follow all rules exactly."
            )

    raise ValueError(
        f"Quiz generation failed after {max_attempts} attempts"
    ) from last_error

