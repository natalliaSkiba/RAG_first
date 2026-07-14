import json
import unittest

from src.quiz.parser import parse_quiz_response


class ParseQuizResponseTest(unittest.TestCase):
    """Tests quiz JSON parsing.."""

    def test_should_parse_valid_quiz(self) -> None:
        response_text = json.dumps(
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
                        "explanation": "L'agent doit protéger la circulation.",
                        "memory_tip": "Danger → protéger",
                        "source_chunk_ids": ["chunk_001"],
                        "evidence": "L'agent doit protéger la circulation.",
                    }
                ],
            }
        )

        quiz = parse_quiz_response(response_text)

        self.assertEqual("Détresse", quiz.topic)
        self.assertEqual(1, len(quiz.questions))
        self.assertEqual(
            "Que doit faire l'agent ?",
            quiz.questions[0].question,
        )
        self.assertEqual(
            1,
            quiz.questions[0].correct_option_index,
        )

    def test_should_reject_invalid_json(self) -> None:
        with self.assertRaises(ValueError):
            parse_quiz_response("not json")

    def test_should_reject_question_without_four_options(self) -> None:
        response_text = json.dumps(
            {
                "topic": "Détresse",
                "questions": [
                    {
                        "question": "Question",
                        "options": ["A", "B"],
                        "correct_option_index": 0,
                        "explanation": "Explanation",
                        "memory_tip": "Tip",
                        "source_chunk_ids": ["chunk_001"],
                        "evidence": "L'agent doit protéger la circulation.",
                    }
                ],
            }
        )

        with self.assertRaises(ValueError):
            parse_quiz_response(response_text)