import unittest

from src.quiz.prompt import build_quiz_prompt


class BuildQuizPromptTest(unittest.TestCase):
    """ Tests quiz prompt creation.."""

    def test_should_build_prompt(self) -> None:
        prompt = build_quiz_prompt(
            topic="Détresse",
            context="CHUNK_ID: chunk_001\nCONTENT: Test content",
            question_count=5,
        )

        self.assertIn("Détresse", prompt)
        self.assertIn("chunk_001", prompt)
        self.assertIn("Return exactly 5 questions", prompt)

    def test_should_reject_empty_topic(self) -> None:
        with self.assertRaises(ValueError):
            build_quiz_prompt(
                topic="",
                context="Valid context",
            )

    def test_should_reject_empty_context(self) -> None:
        with self.assertRaises(ValueError):
            build_quiz_prompt(
                topic="Détresse",
                context="",
            )

    def test_should_reject_invalid_question_count(self) -> None:
        with self.assertRaises(ValueError):
            build_quiz_prompt(
                topic="Détresse",
                context="Valid context",
                question_count=0,
            )