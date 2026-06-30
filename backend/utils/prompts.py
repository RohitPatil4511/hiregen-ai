JD_EXTRACTION_PROMPT = """
You are an expert recruiter. Extract structured information from the job description below.

Return ONLY a JSON object with these exact keys:
- job_title: string
- required_skills: list of strings
- preferred_skills: list of strings
- experience_years: string
- education: string
- responsibilities: list of strings

Job Description:
{jd_text}

Return only valid JSON, nothing else.
"""