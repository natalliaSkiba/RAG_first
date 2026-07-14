import json

from src.quiz.models import Quiz, QuizQuestion


def parse_quiz_response(response_text: str) -> Quiz:
    """ Parses and validates a quiz returned by an LLM."""

    if not response_text.strip():
        raise ValueError("Quiz response must not be empty")

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise ValueError("Quiz response is not valid JSON") from error
    
    if not isinstance(data, dict):
        raise ValueError("Quiz response must be a JSON object")

    topic = str(data.get("topic", "")).strip()
    raw_questions = data.get("questions")

    if not topic:
        raise ValueError("Quiz topic must not be empty")

    if not isinstance(raw_questions, list) or not raw_questions:
        raise ValueError("Quiz must contain questions")

    questions: list[QuizQuestion] = []

    for index, raw_question in enumerate(raw_questions, start=1):
        if not isinstance(raw_question, dict):
            raise ValueError(f"Question {index} must be an object")

        question = str(raw_question.get("question", "")).strip()
        options = raw_question.get("options")
        correct_option_index = raw_question.get("correct_option_index")
        explanation = str(raw_question.get("explanation", "")).strip()
        memory_tip = str(raw_question.get("memory_tip", "")).strip()
        evidence = str(raw_question.get("evidence", "")).strip()
        source_chunk_ids = raw_question.get("source_chunk_ids")

        if not question:
            raise ValueError(f"Question {index} text must not be empty")

        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {index} must contain exactly 4 options")

        cleaned_options = [str(option).strip() for option in options]

        if any(not option for option in cleaned_options):
            raise ValueError(f"Question {index} contains an empty option")

        if not isinstance(correct_option_index, int):
            raise ValueError(
                f"Question {index} correct option index must be an integer"
            )

        if correct_option_index not in range(4):
            raise ValueError(
                f"Question {index} correct option index must be between 0 and 3"
            )

        if not explanation:
            raise ValueError(f"Question {index} explanation must not be empty")

        if not memory_tip:
            raise ValueError(f"Question {index} memory tip must not be empty")

        if not evidence:
            raise ValueError(f"Question {index} evidence must not be empty")

        if not isinstance(source_chunk_ids, list) or not source_chunk_ids:
            raise ValueError(
                f"Question {index} must contain source chunk IDs"
            )

        cleaned_source_ids = [
            str(chunk_id).strip()
            for chunk_id in source_chunk_ids
        ]

        if any(not chunk_id for chunk_id in cleaned_source_ids):
            raise ValueError(
                f"Question {index} contains an empty source chunk ID"
            )

        questions.append(
            QuizQuestion(
                question=question,
                options=cleaned_options,
                correct_option_index=correct_option_index,
                explanation=explanation,
                memory_tip=memory_tip,
                evidence=evidence,
                source_chunk_ids=cleaned_source_ids,
            )
        )

    return Quiz(
        topic=topic,
        questions=questions,
    )