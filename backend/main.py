from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil, os, tempfile

app = FastAPI(title="HireGen AI", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "HireGen AI v3 is running"}

@app.post("/analyze")
async def analyze(
    jd_file: UploadFile = File(...),
    resume_file: UploadFile = File(...)
):
    from backend.agents.jd_agent import extract_jd
    from backend.agents.resume_agent import extract_resume
    from backend.agents.matcher_agent import calculate_fit_score
    from backend.agents.skill_gap_agent import identify_skill_gaps
    from backend.agents.interview_agent import generate_questions

    jd_path = f"{UPLOAD_DIR}/{jd_file.filename}"
    resume_path = f"{UPLOAD_DIR}/{resume_file.filename}"

    with open(jd_path, "wb") as f:
        shutil.copyfileobj(jd_file.file, f)
    with open(resume_path, "wb") as f:
        shutil.copyfileobj(resume_file.file, f)

    jd_data = extract_jd(jd_path)
    resume_data = extract_resume(resume_path)
    match_result = calculate_fit_score(jd_data, resume_data)
    gap_result = identify_skill_gaps(jd_data, resume_data, match_result)
    questions = generate_questions(jd_data, resume_data, gap_result)

    return {
        "jd": jd_data,
        "resume": resume_data,
        "match": match_result,
        "gaps": gap_result,
        "questions": questions.get("questions", [])
    }

@app.post("/analyze-multiple")
async def analyze_multiple(
    jd_file: UploadFile = File(...),
    resume_files: List[UploadFile] = File(...)
):
    from backend.agents.jd_agent import extract_jd
    from backend.agents.resume_agent import extract_multiple_resumes
    from backend.agents.matcher_agent import rank_candidates
    from backend.agents.skill_gap_agent import identify_skill_gaps

    jd_path = f"{UPLOAD_DIR}/{jd_file.filename}"
    with open(jd_path, "wb") as f:
        shutil.copyfileobj(jd_file.file, f)

    resume_paths = []
    for rf in resume_files:
        path = f"{UPLOAD_DIR}/{rf.filename}"
        with open(path, "wb") as f:
            shutil.copyfileobj(rf.file, f)
        resume_paths.append(path)

    jd_data = extract_jd(jd_path)
    resumes = extract_multiple_resumes(resume_paths)
    rankings = rank_candidates(jd_data, resumes)

    enriched = []
    for r in rankings:
        resume = r["resume_data"]
        gaps = identify_skill_gaps(jd_data, resume, r)
        enriched.append({**r, "gaps": gaps, "resume_data": {
            k: v for k, v in resume.items() if not k.startswith("_")
        }})

    return {"jd": jd_data, "rankings": enriched}

@app.post("/evaluate")
async def evaluate(data: dict):
    from backend.agents.evaluator_agent import evaluate_answer
    return evaluate_answer(data.get("question"), data.get("answer"))

@app.post("/chat")
async def chat(data: dict):
    from backend.agents.chatbot_agent import chat_with_recruiter
    question = data.get("question", "")
    history = data.get("history", [])
    answer = chat_with_recruiter(question, history)
    return {"answer": answer}

@app.post("/transcribe")
async def transcribe(audio_file: UploadFile = File(...)):
    """Receive audio file and return transcribed text."""
    from backend.utils.voice import transcribe_audio

    # Save uploaded audio to temp file
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    shutil.copyfileobj(audio_file.file, tmp)
    tmp.close()

    text = transcribe_audio(tmp.name)
    return {"text": text}
@app.post("/generate-report")
async def generate_report(data: dict):
    from backend.utils.pdf_report import generate_pdf_report
    from fastapi.responses import FileResponse

    pdf_path = generate_pdf_report(data)
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"HireGen_Report_{data.get('candidate_name', 'candidate').replace(' ', '_')}.pdf"
    )