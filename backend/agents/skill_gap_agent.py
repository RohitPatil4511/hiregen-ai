from backend.utils.llm import get_llm

llm = get_llm()
SKILL_GAP_PROMPT = """
You are an expert recruiter. Based on the job requirements and candidate skills below, identify the skill gaps.

Required skills for the job: {required_skills}
Candidate's skills: {candidate_skills}
Matched skills: {matched_skills}

Return ONLY a JSON object with these exact keys:
- missing_skills: list of strings (skills in job requirements but not in candidate profile)
- weak_areas: list of strings (skills that partially match but need improvement)
- recommendations: list of strings (what the candidate should learn or improve)
- overall_assessment: string (1-2 sentences summary)

Return only valid JSON, nothing else.
"""

def identify_skill_gaps(jd_data: dict, resume_data: dict, match_result: dict) -> dict:
    import json

    prompt = SKILL_GAP_PROMPT.format(
        required_skills=jd_data.get("required_skills", []),
        candidate_skills=resume_data.get("skills", []),
        matched_skills=match_result.get("matched_skills", [])
    )

    response = llm.invoke(prompt)

    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        start = response.find("{")
        end = response.rfind("}") + 1
        result = json.loads(response[start:end])

    return result