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