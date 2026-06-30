import json
from backend.utils.llm import get_llm

llm = get_llm()
EVAL_PROMPT = """
You are an expert technical interviewer evaluating a candidate's answer.

Question: {question}
Expected key points: {expected_points}
Candidate's answer: {answer}

Evaluate the answer and return ONLY a JSON object with these exact keys:
- score: number from 0 to 10
- feedback: string (2-3 sentences of constructive feedback)
- covered_points: list of strings (expected points the candidate covered)
- missed_points: list of strings (expected points the candidate missed)

Even if the answer is "no", "skip", or very short, still return valid JSON with score 0.

Return only valid JSON, nothing else.
"""

def evaluate_answer(question: dict, answer: str) -> dict:
    # Handle empty or very short answers immediately
    if not answer or answer.lower() in ["no", "n", "idk", "i don't know", "dont know"]:
        return {
            "question_id": question.get("id"),
            "question": question.get("question"),
            "score": 0,
            "feedback": "No answer provided. This is a key area to study before the interview.",
            "covered_points": [],
            "missed_points": question.get("expected_answer_points", [])
        }

    prompt = EVAL_PROMPT.format(
        question=question.get("question", ""),
        expected_points=question.get("expected_answer_points", []),
        answer=answer
    )

    response = llm.invoke(prompt)

    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            result = json.loads(response[start:end])
        except Exception:
            result = {
                "score": 0,
                "feedback": "Could not evaluate answer. Please try again.",
                "covered_points": [],
                "missed_points": question.get("expected_answer_points", [])
            }

    result["question_id"] = question.get("id")
    result["question"] = question.get("question")
    return result


def run_interview(questions: list) -> list:
    evaluations = []
    print("\n=== AI INTERVIEW STARTED ===")
    print("Type your answer and press Enter. Type 'skip' to skip a question.\n")

    for q in questions:
        print(f"\nQ{q['id']} [{q['type'].upper()}] - {q['topic']}")
        print(f"{q['question']}")
        answer = input("Your answer: ").strip()

        if answer.lower() == "skip":
            print("Skipped.")
            continue

        print("Evaluating...")
        evaluation = evaluate_answer(q, answer)
        evaluations.append(evaluation)

        print(f"Score: {evaluation['score']}/10")
        print(f"Feedback: {evaluation['feedback']}")

    return evaluations