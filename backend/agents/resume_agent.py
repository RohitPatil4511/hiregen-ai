import json
import re
import numpy as np
from backend.utils.llm import get_llm
from backend.utils.parser import parse_file
from backend.rag.embeddings import get_embedding
from backend.rag.vectorstore import save_to_vectorstore

llm = get_llm()

RESUME_PROMPT = """
You are an expert recruiter. Extract structured information from the resume below.

Return ONLY a JSON object with these exact keys:
- candidate_name: string
- email: string
- skills: list of strings
- experience_years: string
- education: string
- previous_roles: list of strings
- summary: string (2-3 sentences about the candidate)

Resume:
{resume_text}

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
            "candidate_name": "Unknown",
            "email": "",
            "skills": [],
            "experience_years": "0",
            "education": "",
            "previous_roles": [],
            "summary": ""
        }

def extract_resume(file_path: str) -> dict:
    text = parse_file(file_path)
    prompt = RESUME_PROMPT.format(resume_text=text)
    response = llm.invoke(prompt)
    result = clean_and_parse_json(response)
    result["_raw_text"] = text
    result["_file_path"] = file_path
    embedding = get_embedding(text).reshape(1, -1)
    save_to_vectorstore(embedding, [result])
    return result

def extract_multiple_resumes(file_paths: list) -> list:
    results = []
    for path in file_paths:
        print(f"  Processing: {path}")
        result = extract_resume(path)
        results.append(result)
    return results