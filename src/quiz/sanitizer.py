from dataclasses import replace

from src.quiz.models import Quiz


def sanitize_quiz(quiz: Quiz) -> Quiz:
    """ Replaces potentially invented explanations with grounded text. """

    safe_questions = []

    for question in quiz.questions:
        correct_answer = question.options[
            question.correct_option_index
        ]

        safe_questions.append(
            replace(
                question,
                explanation=f"Le texte indique : {question.evidence}",
                memory_tip=f"À retenir : {correct_answer}",
            )
        )

    return replace(
        quiz,
        questions=safe_questions,
    )