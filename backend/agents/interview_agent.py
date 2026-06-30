import json
import re
from backend.utils.llm import get_llm

llm = get_llm()
INTERVIEW_PROMPT = """
You are an expert technical interviewer. Generate interview questions for a candidate.

Job Title: {job_title}
Required Skills: {required_skills}
Candidate Skills: {candidate_skills}
Skill Gaps: {missing_skills}
Weak Areas: {weak_areas}

Generate exactly 6 interview questions:
- 2 technical questions about their strong skills
- 2 questions targeting their skill gaps
- 2 behavioral questions

Return ONLY valid JSON in this format:
{{"questions": [{{"id": 1, "type": "technical", "topic": "FastAPI", "question": "Your question here?", "expected_answer_points": ["point1", "point2"]}}]}}

No extra text, no markdown, just JSON.
"""

FALLBACK_QUESTIONS = {
    "questions": [
        {"id": 1, "type": "technical", "topic": "FastAPI", "question": "How does FastAPI handle request validation?", "expected_answer_points": ["Pydantic models", "type hints", "automatic validation"]},
        {"id": 2, "type": "technical", "topic": "Docker", "question": "How do Docker containers help in deployment?", "expected_answer_points": ["isolation", "portability", "images", "containers"]},
        {"id": 3, "type": "technical", "topic": "Kubernetes", "question": "What is a Kubernetes pod?", "expected_answer_points": ["smallest unit", "containers", "networking", "lifecycle"]},
        {"id": 4, "type": "technical", "topic": "PostgreSQL", "question": "How do database indexes improve query performance?", "expected_answer_points": ["B-tree", "faster lookup", "trade-offs"]},
        {"id": 5, "type": "behavioral", "topic": "Teamwork", "question": "Tell me about a time you solved a difficult technical problem in a team.", "expected_answer_points": ["collaboration", "communication", "outcome"]},
        {"id": 6, "type": "behavioral", "topic": "Learning", "question": "How do you keep up with new technologies?", "expected_answer_points": ["self learning", "resources", "practice"]}
    ]
}

def generate_questions(jd_data: dict, resume_data: dict, gap_data: dict) -> dict:
    prompt = INTERVIEW_PROMPT.format(
        job_title=jd_data.get("job_title", ""),
        required_skills=jd_data.get("required_skills", []),
        candidate_skills=resume_data.get("skills", []),
        missing_skills=gap_data.get("missing_skills", []),
        weak_areas=gap_data.get("weak_areas", [])
    )
    response = llm.invoke(prompt)
    cleaned = re.sub(r"```json|```", "", response).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        try:
            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1
            return json.loads(cleaned[start:end])
        except Exception:
            print("Warning: Using fallback questions.")
            return FALLBACK_QUESTIONS
