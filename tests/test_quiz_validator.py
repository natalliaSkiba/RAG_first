import unittest

from src.quiz.models import Quiz, QuizQuestion
from src.quiz.validator import validate_quiz_sources


class ValidateQuizSourcesTest(unittest.TestCase):
    """Tests quiz source and evidence validation."""

    def test_should_accept_existing_evidence(self) -> None:
        quiz = Quiz(
            topic="Détresse",
            questions=[
                QuizQuestion(
                    question="Que doit faire l'agent ?",
                    options=["Attendre", "Protéger", "Partir", "Ignorer"],
                    correct_option_index=1,
                    explanation="L'agent doit protéger la circulation.",
                    memory_tip="Danger → protéger",
                    source_chunk_ids=["chunk_001"],
                    evidence="L'agent doit protéger la circulation.",
                )
            ],
        )

        validate_quiz_sources(
            quiz=quiz,
            source_texts={
                "chunk_001": "L'agent doit protéger la circulation."
            },
        )

    def test_should_reject_unknown_chunk_id(self) -> None:
        quiz = Quiz(
            topic="Détresse",
            questions=[
                QuizQuestion(
                    question="Que doit faire l'agent ?",
                    options=["A", "B", "C", "D"],
                    correct_option_index=1,
                    explanation="Explication",
                    memory_tip="À retenir",
                    source_chunk_ids=["chunk_unknown"],
                    evidence="Texte source.",
                )
            ],
        )

        with self.assertRaises(ValueError):
            validate_quiz_sources(
                quiz=quiz,
                source_texts={
                    "chunk_001": "Texte source."
                },
            )

    def test_should_reject_evidence_not_found_in_source(self) -> None:
        quiz = Quiz(
            topic="Détresse",
            questions=[
                QuizQuestion(
                    question="Que doit faire l'agent ?",
                    options=["A", "B", "C", "D"],
                    correct_option_index=1,
                    explanation="Explication",
                    memory_tip="À retenir",
                    source_chunk_ids=["chunk_001"],
                    evidence="Cette phrase est inventée.",
                )
            ],
        )

        with self.assertRaises(ValueError):
            validate_quiz_sources(
                quiz=quiz,
                source_texts={
                    "chunk_001": "L'agent doit protéger la circulation."
                },
            )

    def test_should_reject_correct_option_not_supported_by_evidence(
            self,
    ) -> None:
        quiz = Quiz(
            topic="Détresse",
            questions=[
                QuizQuestion(
                    question="Que doit faire l'agent ?",
                    options=[
                        "Attendre",
                        "Protéger la circulation",
                        "Déclencher une inondation",
                        "Partir",
                    ],
                    correct_option_index=2,
                    explanation="Explication",
                    memory_tip="À retenir",
                    source_chunk_ids=["chunk_001"],
                    evidence=(
                        "En cas de danger grave, l'agent doit "
                        "protéger la circulation et donner l'alerte."
                    ),
                )
            ],
        )

        with self.assertRaises(ValueError):
            validate_quiz_sources(
                quiz=quiz,
                source_texts={
                    "chunk_001": (
                        "En cas de danger grave, l'agent doit "
                        "protéger la circulation et donner l'alerte."
                    )
                },
            )
