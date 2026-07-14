from dataclasses import dataclass


@dataclass(frozen=True)
class QuizQuestion:
    """Represents one generated multiple-choice quiz question."""

    question: str
    options: list[str]
    correct_option_index: int
    explanation: str
    memory_tip: str
    source_chunk_ids: list[str]
    evidence: str


@dataclass(frozen=True)
class Quiz:
    """ Represents a quiz generated for one learning topic."""

    topic: str
    questions: list[QuizQuestion]