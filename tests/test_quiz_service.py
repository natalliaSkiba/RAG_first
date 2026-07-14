import json
import unittest

from src.quiz.service import generate_quiz
from src.retrieval.models import (
    HybridSearchResult,
    RetrievalRecord,
)


class FakeQuizGenerator:
    """Fake generator for tests."""

    def generate(self, prompt: str) -> str:
        return json.dumps(
            {
                "topic": "Détresse",
                "questions": [
                    {
                        "question": "Que doit faire l'agent ?",
                        "options": [
                            "Attendre",
                            "Protéger",
                            "Partir",
                            "Ignorer",
                        ],
                        "correct_option_index": 1,
                        "explanation": (
                            "L'agent doit protéger la circulation."
                        ),
                        "memory_tip": "Danger → protéger",
                        "evidence": (
                            "L'agent doit protéger la circulation."
                        ),
                        "source_chunk_ids": ["chunk_001"],
                    }
                ],
            }
        )


class RetryQuizGenerator:
    """Returns an invalid quiz first, then a valid quiz."""

    def __init__(self) -> None:
        self.call_count = 0

    def generate(self, prompt: str) -> str:
        self.call_count += 1

        if self.call_count == 1:
            return json.dumps(
                {
                    "topic": "Détresse",
                    "questions": [
                        {
                            "question": "Quand agir ?",
                            "options": [
                                "Attendre",
                                "Partir",
                                "En cas d'inondation",
                                "Ignorer",
                            ],
                            "correct_option_index": 2,
                            "explanation": "Explication",
                            "memory_tip": "À retenir",
                            "evidence": (
                                "L'agent doit protéger la circulation."
                            ),
                            "source_chunk_ids": ["chunk_001"],
                        }
                    ],
                }
            )

        return json.dumps(
            {
                "topic": "Détresse",
                "questions": [
                    {
                        "question": "Que doit faire l'agent ?",
                        "options": [
                            "Attendre",
                            "Protéger la circulation",
                            "Partir",
                            "Ignorer",
                        ],
                        "correct_option_index": 1,
                        "explanation": (
                            "L'agent doit protéger la circulation."
                        ),
                        "memory_tip": "Danger → protéger",
                        "evidence": (
                            "L'agent doit protéger la circulation."
                        ),
                        "source_chunk_ids": ["chunk_001"],
                    }
                ],
            }
        )


class GenerateQuizTest(unittest.TestCase):

    def test_should_generate_quiz_from_search_results(self) -> None:
        record = RetrievalRecord(
            chunk_id="chunk_001",
            text="L'agent doit protéger la circulation.",
            embedding=[],
            metadata={"heading": "Détresse"},
            embedding_metadata={},
        )

        result = HybridSearchResult(
            rank=1,
            score=0.9,
            semantic_score=0.8,
            keyword_score=0.1,
            record=record,
        )

        quiz = generate_quiz(
            generator=FakeQuizGenerator(),
            topic="Détresse",
            search_results=[result],
            question_count=1,
        )

        self.assertEqual("Détresse", quiz.topic)
        self.assertEqual(1, len(quiz.questions))
        self.assertEqual(
            "Que doit faire l'agent ?",
            quiz.questions[0].question,
        )

    def test_should_retry_after_invalid_quiz(self) -> None:
        record = RetrievalRecord(
            chunk_id="chunk_001",
            text="L'agent doit protéger la circulation.",
            embedding=[],
            metadata={"heading": "Détresse"},
            embedding_metadata={},
        )

        result = HybridSearchResult(
            rank=1,
            score=0.9,
            semantic_score=0.8,
            keyword_score=0.1,
            record=record,
        )

        generator = RetryQuizGenerator()

        self.quiz = generate_quiz(generator=generator, topic="Détresse", search_results=[result], question_count=1,
                                  max_attempts=2, )
        quiz = self.quiz

        self.assertEqual(2, generator.call_count)

        correct_answer = quiz.questions[0].options[
            quiz.questions[0].correct_option_index
        ]

        self.assertEqual(
            "Protéger la circulation",
            correct_answer,
        )
