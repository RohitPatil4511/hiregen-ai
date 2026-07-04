---
title: HireGen AI
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# 🤖 HireGen AI — Multi-Agent Recruitment Copilot

> An end-to-end AI recruitment system that screens candidates, scores fit, conducts AI interviews, and generates hiring reports — fully automated by 6 coordinated AI agents.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-8A2BE2?style=flat-square)
![Llama](https://img.shields.io/badge/Llama-3.2-FF6F00?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=flat-square&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 Overview

Recruiters spend hours manually screening resumes, comparing candidates against job requirements, and conducting first-round interviews. **HireGen AI automates this entire workflow.**

A recruiter uploads a **Job Description** and one or more **Resumes**. The system runs them through a 6-agent AI pipeline that extracts, matches, interviews, and evaluates candidates — producing a final **HIRE / MAYBE / NO HIRE** decision with a downloadable PDF report, in minutes instead of hours.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Multi-Agent Pipeline** | 6 specialized AI agents orchestrated via LangGraph, each handling one stage of the hiring workflow |
| 🔍 **Semantic + Keyword Matching** | RAG-based fit scoring using FAISS + Sentence Transformers, combined with keyword overlap for a robust 0–100 score |
| 🎯 **Skill Gap Analysis** | Automatically identifies missing skills, weak areas, and generates personalized upskilling recommendations |
| 🗣️ **AI Interview (Text)** | Generates 6–8 targeted interview questions based on the candidate's specific skill gaps, then evaluates typed answers in real time |
| 🎤 **AI Interview (Voice)** | Candidates speak their answers — Whisper transcribes speech to text, which feeds directly into the LLM evaluator |
| 📊 **Candidate Comparison** | Upload multiple resumes against one JD to get a ranked leaderboard of all candidates |
| 💬 **Recruiter Chatbot** | Ask natural-language questions like *"Who has the strongest Python skills?"* — answered via RAG over all analyzed candidates |
| 📄 **PDF Hiring Reports** | One-click professional PDF export with scores, skills breakdown, interview transcript, and final decision |
| 🐳 **Docker Ready** | Fully containerized for one-command local deployment or cloud hosting |

---

## 🏗️ Architecture
                Recruiter
                    │
                    ▼
          Streamlit UI (Frontend)
                    │
                    ▼
           FastAPI (Backend API)
                    │
                    ▼
        LangGraph Multi-Agent Workflow
                   │
                   ▼
        Final Hiring Report (+ PDF)

### Agent Pipeline Detail

| Step | Agent | Input | Output |
|---|---|---|---|
| 1 | **JD Agent** | Job description (PDF/TXT) | Required skills, experience level, responsibilities |
| 2 | **Resume Agent** | Candidate resume(s) | Structured profile + FAISS embedding for RAG |
| 3 | **Match Agent** | JD + Resume data | Fit score (semantic + keyword, 0–100) |
| 4 | **Skill Gap Agent** | Match results | Missing skills, weak areas, recommendations |
| 5 | **Interview Agent** | Gaps + candidate profile | 6–8 targeted interview questions |
| 6 | **Evaluator Agent** | Candidate answers | Per-question score, feedback, final report |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Llama 3.2 (via [Ollama](https://ollama.com), local) / Groq API (cloud deployment) |
| **Agent Orchestration** | LangGraph + LangChain |
| **RAG / Vector Search** | FAISS + Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Backend** | FastAPI |
| **Frontend** | Streamlit + Plotly |
| **Voice AI** | Faster-Whisper (speech-to-text) |
| **PDF Generation** | ReportLab |
| **Deployment** | Docker, Docker Compose, Hugging Face Spaces |

---

## 🚀 Quick Start (Local — Ollama)

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com) installed

### 1. Clone the repository
```bash
git clone https://github.com/RohitPatil4511/hiregen-ai.git
cd hiregen-ai
```

### 2. Set up a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Pull the Llama model
```bash
ollama pull llama3.2
```

### 5. Run the app

**Terminal 1 — Backend:**
```bash
uvicorn backend.main:app --reload
```

**Terminal 2 — Frontend:**
```bash
streamlit run frontend/app.py
```

Open your browser at **`http://localhost:8501`**

---

## 🐳 Run with Docker

```bash
docker-compose up
```

This spins up FastAPI, Streamlit, and Ollama in separate containers automatically.

---

## ☁️ Cloud Deployment (Groq API)

For deployments where running Ollama isn't practical (e.g. free-tier hosting), the app automatically switches to the [Groq API](https://console.groq.com) — same Llama model family, hosted inference, no local GPU/CPU load.

```bash
export USE_GROQ=true
export GROQ_API_KEY=your_key_here
```

The app detects this automatically via `backend/utils/llm.py` — no code changes needed between local and cloud modes.

---

## 📂 Project Structure
hiregen-ai/
│
├── backend/
│   ├── main.py                 # FastAPI app + routes
│   ├── agents/
│   │   ├── jd_agent.py         # Extracts JD requirements
│   │   ├── resume_agent.py     # Parses resumes + RAG embedding
│   │   ├── matcher_agent.py    # Fit scoring + candidate ranking
│   │   ├── skill_gap_agent.py  # Skill gap analysis
│   │   ├── interview_agent.py  # Interview question generation
│   │   ├── evaluator_agent.py  # Answer evaluation
│   │   └── chatbot_agent.py    # RAG recruiter chatbot
│   ├── graph/
│   │   └── workflow.py         # LangGraph pipeline definition
│   ├── rag/
│   │   ├── embeddings.py       # Sentence Transformer embeddings
│   │   ├── vectorstore.py      # FAISS index management
│   │   └── retriever.py        # Semantic retrieval
│   └── utils/
│       ├── parser.py           # PDF/TXT parsing
│       ├── prompts.py          # LLM prompt templates
│       ├── llm.py              # Ollama/Groq model loader
│       ├── voice.py            # Whisper speech-to-text
│       └── pdf_report.py       # PDF report generation
│
├── frontend/
│   └── app.py                  # Streamlit UI (4 pages)
│
├── data/                       # Uploads + vector store (gitignored)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

---

## 📋 Usage Walkthrough

1. **Single Analysis** — Upload one JD + one resume → get fit score, matched/missing skills, recommendations → take the AI interview → download PDF report
2. **Compare Candidates** — Upload one JD + multiple resumes → see a ranked leaderboard of all candidates
3. **Recruiter Chatbot** — Ask questions about any candidate you've already analyzed
4. **Voice Interview** *(local only)* — Speak your interview answers instead of typing

---

## 🗺️ Roadmap

- [x] Multi-agent LangGraph pipeline
- [x] RAG-based resume matching
- [x] Voice AI interviews (Whisper)
- [x] Recruiter chatbot
- [x] PDF report generation
- [x] Docker + cloud deployment support
- [ ] PostgreSQL persistence + recruiter accounts
- [ ] Multi-language resume support
- [ ] ATS (Applicant Tracking System) integration

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Rohit Patil**
AI/ML Engineer
[LinkedIn](https://www.linkedin.com/in/rohit-patil-261189355/) · [GitHub](https://github.com/RohitPatil4511) · rohitpatil89045@gmail.com

---

<p align="center">Built with LangGraph, Llama 3, and a lot of debugging 🚀</p>
