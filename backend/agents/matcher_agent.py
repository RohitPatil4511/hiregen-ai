from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_fit_score(jd_data: dict, resume_data: dict) -> dict:
    jd_skills = jd_data.get("required_skills", [])
    candidate_skills = resume_data.get("skills", [])

    jd_text = " ".join(jd_skills).lower()
    resume_text = " ".join(candidate_skills).lower()

    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    semantic_score = float(util.cos_sim(jd_embedding, resume_embedding)[0][0])

    jd_skills_lower = [s.lower() for s in jd_skills]
    candidate_skills_lower = [s.lower() for s in candidate_skills]
    matched = [s for s in jd_skills_lower if any(s in cs or cs in s for cs in candidate_skills_lower)]
    keyword_score = len(matched) / len(jd_skills_lower) if jd_skills_lower else 0

    final_score = round((semantic_score * 0.5 + keyword_score * 0.5) * 100, 2)

    return {
        "candidate_name": resume_data.get("candidate_name", "Unknown"),
        "fit_score": final_score,
        "matched_skills": matched,
        "total_required": len(jd_skills_lower),
        "total_matched": len(matched),
        "semantic_score": round(semantic_score * 100, 2),
        "keyword_score": round(keyword_score * 100, 2)
    }


def rank_candidates(jd_data: dict, resumes: list) -> list:
    scores = []
    for resume in resumes:
        score = calculate_fit_score(jd_data, resume)
        score["resume_data"] = resume
        scores.append(score)
    scores.sort(key=lambda x: x["fit_score"], reverse=True)
    for i, s in enumerate(scores):
        s["rank"] = i + 1
    return scores