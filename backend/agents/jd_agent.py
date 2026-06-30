import json
from backend.utils.llm import get_llm
from backend.utils.prompts import JD_EXTRACTION_PROMPT
from backend.utils.parser import parse_file

llm = get_llm()
def extract_jd(file_path: str) -> dict:
    text = parse_file(file_path)
    prompt = JD_EXTRACTION_PROMPT.format(jd_text=text)
    response = llm.invoke(prompt)

    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        start = response.find("{")
        end = response.rfind("}") + 1
        result = json.loads(response[start:end])

    return result