import json
import re
from backend.utils.llm import get_llm

llm = get_llm()

SKILL_GAP_PROMPT = """
You are an expert recruiter. Based on the job requirements and candidate skills below, identify the skill gaps.

Required skills for the job: {required_skills}
Candidate's skills: {candidate_skills}
Matched skills: {matched_skills}

Return ONLY a JSON object with these exact keys:
- missing_skills: list of strings
- weak_areas: list of strings
- recommendations: list of strings
- overall_assessment: string

Return only valid JSON, nothing else.
"""

def clean_and_parse_json(text: str) -> dict:
    text = re.sub(r"```json|```", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except json.JSONDecodeError:
        pass
    try:
        fixed = re.sub(r",\s*([}\]])", r"\1", text)
        start = fixed.find("{")
        end = fixed.rfind("}") + 1
        return json.loads(fixed[start:end])
    except Exception:
        return {
            "missing_skills": [],
            "weak_areas": [],
            "recommendations": [],
            "overall_assessment": "Could not assess"
        }

def identify_skill_gaps(jd_data: dict, resume_data: dict, match_result: dict) -> dict:
    prompt = SKILL_GAP_PROMPT.format(
        required_skills=jd_data.get("required_skills", []),
        candidate_skills=resume_data.get("skills", []),
        matched_skills=match_result.get("matched_skills", [])
    )
    response = llm.invoke(prompt)
    return clean_and_parse_json(response)