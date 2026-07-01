import json
import re
from backend.utils.llm import get_llm
from backend.utils.prompts import JD_EXTRACTION_PROMPT
from backend.utils.parser import parse_file

llm = get_llm()

def clean_and_parse_json(text: str) -> dict:
    """Robustly parse JSON from LLM output."""
    # Remove markdown code blocks
    text = re.sub(r"```json|```", "", text).strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON object
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])
    except json.JSONDecodeError:
        pass

    # Fix common issues: trailing commas before } or ]
    try:
        fixed = re.sub(r",\s*([}\]])", r"\1", text)
        start = fixed.find("{")
        end = fixed.rfind("}") + 1
        return json.loads(fixed[start:end])
    except json.JSONDecodeError:
        pass

    # Return safe default
    return {
        "job_title": "Unknown",
        "required_skills": [],
        "preferred_skills": [],
        "experience_years": "Not specified",
        "education": "Not specified",
        "responsibilities": []
    }

def extract_jd(file_path: str) -> dict:
    text = parse_file(file_path)
    prompt = JD_EXTRACTION_PROMPT.format(jd_text=text)
    response = llm.invoke(prompt)
    return clean_and_parse_json(response)