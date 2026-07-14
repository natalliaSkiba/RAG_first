from src.quiz.ollama_generator import OllamaQuizGenerator
from src.quiz.service import generate_quiz
from src.retrieval.models import (
    HybridSearchResult,
    RetrievalRecord,
)


source_text = (
    "L'AC devra recevoir l'annulation de la demande de secours "
    "du conducteur via le formulaire REMA. "
    "L'AC transmettra alors l'Autorisation de Remise en Marche "
    "au conducteur."
)

record = RetrievalRecord(
    chunk_id="chunk_001",
    text=source_text,
    embedding=[],
    metadata={"heading": "ACDV 130 — Détresse : secours et dégagement"},
    embedding_metadata={},
)

search_result = HybridSearchResult(
    rank=1,
    score=1.0,
    semantic_score=1.0,
    keyword_score=0.0,
    record=record,
)

generator = OllamaQuizGenerator()

quiz = generate_quiz(
    generator=generator,
    topic="Détresse",
    search_results=[search_result],
    question_count=1,
    max_attempts=3,
)

question = quiz.questions[0]
correct_answer = question.options[question.correct_option_index]

print(f"Question: {question.question}")
print(f"Correct answer: {correct_answer}")
print(f"Explanation: {question.explanation}")
print(f"Memory tip: {question.memory_tip}")
print(f"Evidence: {question.evidence}")
print("VALIDATION: OK")