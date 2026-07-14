def build_quiz_prompt(
    topic: str,
    context: str,
    question_count: int = 10,
) -> str:
    """Build instructions for quiz generation."""

    topic = topic.strip()
    context = context.strip()

    if not topic:
        raise ValueError("Topic must not be empty")

    if not context:
        raise ValueError("Context must not be empty")

    if question_count < 1:
        raise ValueError(
            "Question count must be greater than zero"
        )

    return f"""
Create a detailed educational quiz in French.

TOPIC:
{topic}

SOURCE MATERIAL:
{context}

Return exactly {question_count} questions.

Return ONLY valid JSON with this structure:

{{
  "topic": "{topic}",
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_option_index": 0,
      "explanation": "Short and simple explanation",
      "memory_tip": "One short fact to remember",
      "evidence": "Exact sentence copied from SOURCE MATERIAL",
      "source_chunk_ids": ["real_chunk_id"]
    }}
  ]
}}

Rules:

- The quiz is intended only for the preparation of aiguilleurs
  and agents de circulation (AC).

- Each question must test a fact about an action, decision,
  verification, communication, prohibition or responsibility
  assigned in SOURCE MATERIAL to an aiguilleur or an agent
  de circulation.

- Determine the target role only from SOURCE MATERIAL.
  Do not use outside knowledge and do not guess a role.

- Do not treat "aiguilleur" and "agent de circulation" as the
  same role unless SOURCE MATERIAL explicitly does so.

- Other roles may be mentioned in the situation, but the fact
  being tested must concern the duty of the aiguilleur or AC.

- Do not test the duties, definitions or responsibilities of
  conducteurs, chefs de manoeuvre, agents formation or other roles.

- Do not expand an abbreviation unless its full meaning is
  explicitly provided in SOURCE MATERIAL.

- When the source uses "AC", keep "AC". Never invent a meaning
  for this abbreviation.

- The correct option must be a short, exact, contiguous excerpt
  from the evidence.

- Evidence must be the shortest exact contiguous excerpt that
  clearly supports the correct option and the tested duty.

- If SOURCE MATERIAL does not contain enough suitable facts,
  do not invent, repeat or transfer duties from another role.
""".strip()