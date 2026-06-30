import json
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

def extract_resume(file_path: str) -> dict:
    text = parse_file(file_path)
    prompt = RESUME_PROMPT.format(resume_text=text)
    response = llm.invoke(prompt)

    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        start = response.find("{")
        end = response.rfind("}") + 1
        result = json.loads(response[start:end])

    # Store both result and raw text for RAG
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