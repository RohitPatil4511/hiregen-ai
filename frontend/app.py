import streamlit as st
import requests
import plotly.graph_objects as go
import os
API_URL = "http://127.0.0.1:8000"

# --- Page config ---
st.set_page_config(
    page_title="HireGen AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Force all text visible */
    .stApp, .stApp p, .stApp div, .stApp span, .stApp label {
        color: #e5e7eb !important;
    }
    
    /* Main background */
    .stApp { background-color: #0f1117; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1a1d27 !important;
        border-right: 1px solid #2d2f3e;
    }
    [data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    /* Radio buttons */
    .stRadio label { color: #e5e7eb !important; }
    .stRadio div { color: #e5e7eb !important; }

    /* All headings */
    h1, h2, h3, h4, h5, h6 { color: #f9fafb !important; }

    /* Input labels */
    label { color: #9ca3af !important; }

    /* Text area and inputs */
    .stTextArea textarea, .stTextInput input {
        background: #1a1d27 !important;
        color: #e5e7eb !important;
        border: 1px solid #2d2f3e !important;
        border-radius: 8px !important;
    }

    /* Cards */
    .metric-card {
        background: #1a1d27;
        border: 1px solid #2d2f3e;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #9ca3af !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 4px;
    }

    /* Skill tags */
    .skill-tag-green {
        display: inline-block;
        background: #052e16;
        color: #86efac !important;
        border: 1px solid #166534;
        border-radius: 999px;
        padding: 3px 12px;
        font-size: 0.8rem;
        margin: 3px;
    }
    .skill-tag-red {
        display: inline-block;
        background: #2d0a0a;
        color: #fca5a5 !important;
        border: 1px solid #7f1d1d;
        border-radius: 999px;
        padding: 3px 12px;
        font-size: 0.8rem;
        margin: 3px;
    }
    .skill-tag-yellow {
        display: inline-block;
        background: #1c1500;
        color: #fde68a !important;
        border: 1px solid #78350f;
        border-radius: 999px;
        padding: 3px 12px;
        font-size: 0.8rem;
        margin: 3px;
    }

    /* Decision banners */
    .decision-hire {
        background: linear-gradient(135deg, #052e16, #065f46);
        border: 1px solid #10b981;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #10b981 !important;
        letter-spacing: 0.05em;
    }
    .decision-maybe {
        background: linear-gradient(135deg, #1c1500, #292524);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #f59e0b !important;
        letter-spacing: 0.05em;
    }
    .decision-nohire {
        background: linear-gradient(135deg, #2d0a0a, #1c0a0a);
        border: 1px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #ef4444 !important;
        letter-spacing: 0.05em;
    }

    /* Section headers */
    .section-header {
        font-size: 0.7rem;
        font-weight: 600;
        color: #6b7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin: 24px 0 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #2d2f3e;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #1a1d27 !important;
        color: #e5e7eb !important;
        border: 1px solid #2d2f3e !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        background: #1a1d27 !important;
        border: 1px solid #2d2f3e !important;
        color: #e5e7eb !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #5a6fd6, #6a3f96) !important;
        color: white !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: #1a1d27 !important;
        border: 1px solid #2d2f3e !important;
        border-radius: 12px !important;
        color: #e5e7eb !important;
    }

    /* Info / success / error boxes */
    .stAlert { border-radius: 8px !important; }

    /* Upload area */
    /* Upload area */
    [data-testid="stFileUploader"] {
        background: #1a1d27 !important;
        border: 1px dashed #2d2f3e !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploader"] * {
        color: #9ca3af !important;
        background: #1a1d27 !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: #1a1d27 !important;
        border: 1px dashed #374151 !important;
        border-radius: 10px !important;
    }
    [data-testid="stFileUploaderDropzone"] * {
        color: #6b7280 !important;
        background: transparent !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: #2d2f3e !important;
        color: #e5e7eb !important;
        border: 1px solid #374151 !important;
        border-radius: 6px !important;
    }
    section[data-testid="stFileUploadDropzone"] {
        background: #1a1d27 !important;
    }

    /* Spinner */
    .stSpinner { color: #667eea !important; }

    /* Hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)# --- Radar chart ---
def make_radar(fit, interview, keyword, semantic):
    fig = go.Figure()
    categories = ["Fit Score", "Interview", "Keyword Match", "Semantic Match", "Overall"]
    overall = round((fit * 0.6 + interview * 10 * 0.4), 1)
    values = [fit, interview * 10, keyword, semantic, overall]

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(102,126,234,0.15)",
        line=dict(color="#667eea", width=2),
        name="Candidate"
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="#1a1d27",
            radialaxis=dict(
                visible=True, range=[0, 100],
                tickfont=dict(color="#6b7280", size=10),
                gridcolor="#2d2f3e", linecolor="#2d2f3e"
            ),
            angularaxis=dict(
                tickfont=dict(color="#9ca3af", size=11),
                gridcolor="#2d2f3e", linecolor="#2d2f3e"
            )
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        height=300
    )
    return fig

def make_bar(matched, missing):
    all_skills = [(s, True) for s in matched] + [(s, False) for s in missing]
    labels = [s[0] for s in all_skills]
    colors = ["#10b981" if s[1] else "#ef4444" for s in all_skills]
    values = [1] * len(all_skills)

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker_color=colors,
        text=["✓ matched" if s[1] else "✗ missing" for s in all_skills],
        textposition="inside",
        textfont=dict(color="white", size=11)
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(tickfont=dict(color="#9ca3af", size=11)),
        margin=dict(l=10, r=10, t=10, b=10),
        height=max(200, len(all_skills) * 32)
    )
    return fig

# --- Session init ---
for key, val in {
    "analysis_done": False, "result": None,
    "evaluations": [], "current_q": 0,
    "interview_done": False, "chat_history": [],
    "voice_step": "upload", "voice_result": None,
    "voice_questions": [], "voice_q_idx": 0, "voice_evals": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🤖 HireGen AI")
    st.markdown("<div style='color:#6b7280;font-size:0.8rem;margin-bottom:1.5rem'>Multi-Agent Recruitment Copilot</div>", unsafe_allow_html=True)
    st.markdown("---")
    pages = ["🔍  Single Analysis", "📊  Compare Candidates", "💬  Recruiter Chatbot"]
if os.getenv("USE_GROQ", "false").lower() != "true":
    pages.append("🎤  Voice Interview")  # Voice only available locally

page = st.radio("", pages, label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='color:#6b7280;font-size:0.75rem'>Powered by</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#9ca3af;font-size:0.8rem'>Llama 3.2 · LangGraph · FAISS</div>", unsafe_allow_html=True)

# ============================================================
# PAGE 1: SINGLE ANALYSIS
# ============================================================
if "Single" in page:
    st.markdown("# 🔍 Single Candidate Analysis")
    st.markdown("<div style='color:#6b7280;margin-bottom:2rem'>Upload a job description and resume for deep AI analysis + interview</div>", unsafe_allow_html=True)

    if not st.session_state.analysis_done:
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("<div class='section-header'>Job Description</div>", unsafe_allow_html=True)
            jd_file = st.file_uploader("", type=["pdf", "txt"], key="jd", label_visibility="collapsed")
        with col2:
            st.markdown("<div class='section-header'>Candidate Resume</div>", unsafe_allow_html=True)
            resume_file = st.file_uploader("", type=["pdf", "txt"], key="resume", label_visibility="collapsed")

        if jd_file and resume_file:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀  Run AI Pipeline", use_container_width=True):
                with st.spinner(""):
                    bar = st.progress(0, "Extracting job description...")
                    files = {
                        "jd_file": (jd_file.name, jd_file.getvalue()),
                        "resume_file": (resume_file.name, resume_file.getvalue())
                    }
                    bar.progress(20, "Analyzing resume...")
                    try:
                        response = requests.post(f"{API_URL}/analyze", files=files, timeout=300)
                        bar.progress(60, "Matching skills...")
                        if response.status_code == 200:
                            bar.progress(80, "Generating interview questions...")
                            st.session_state.result = response.json()
                            bar.progress(100, "Done!")
                            st.session_state.analysis_done = True
                            st.rerun()
                        else:
                            st.error(f"API Error: {response.text}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")

    if st.session_state.analysis_done and st.session_state.result:
        result = st.session_state.result
        match = result.get("match", {})
        gaps = result.get("gaps", {})
        resume = result.get("resume", {})
        jd = result.get("jd", {})
        questions = result.get("questions", [])

        # Candidate header
        st.markdown(f"""
        <div style='background:#1a1d27;border:1px solid #2d2f3e;border-radius:12px;padding:20px;margin-bottom:1.5rem'>
            <div style='font-size:1.4rem;font-weight:700;color:#f9fafb'>{resume.get('candidate_name', 'Candidate')}</div>
            <div style='color:#6b7280;font-size:0.9rem;margin-top:4px'>Applying for: <span style='color:#667eea'>{jd.get('job_title', 'Role')}</span> &nbsp;·&nbsp; {resume.get('experience_years', '?')} years exp &nbsp;·&nbsp; {resume.get('education', '')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Score cards
        fit = match.get("fit_score", 0)
        avg = round(sum(e["score"] for e in st.session_state.evaluations) / len(st.session_state.evaluations), 1) if st.session_state.evaluations else 0
        overall = round((fit * 0.6 + avg * 10 * 0.4), 1)

        col1, col2, col3, col4 = st.columns(4)
        for col, val, label in [
            (col1, f"{fit}", "Fit Score / 100"),
            (col2, f"{match.get('semantic_score', 0)}", "Semantic Match"),
            (col3, f"{match.get('keyword_score', 0)}", "Keyword Match"),
            (col4, f"{match.get('total_matched', 0)}/{match.get('total_required', 0)}", "Skills Matched")
        ]:
            col.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Radar + Skills bar
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("<div class='section-header'>Score Radar</div>", unsafe_allow_html=True)
            st.plotly_chart(
                make_radar(fit, avg, match.get("keyword_score", 0), match.get("semantic_score", 0)),
                use_container_width=True, config={"displayModeBar": False}
            )
        with col2:
            st.markdown("<div class='section-header'>Skills Breakdown</div>", unsafe_allow_html=True)
            st.plotly_chart(
                make_bar(match.get("matched_skills", []), gaps.get("missing_skills", [])),
                use_container_width=True, config={"displayModeBar": False}
            )

        # Skills tags
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='section-header'>Matched Skills</div>", unsafe_allow_html=True)
            tags = "".join(f"<span class='skill-tag-green'>{s}</span>" for s in match.get("matched_skills", []))
            st.markdown(tags or "<span style='color:#6b7280'>None</span>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='section-header'>Missing Skills</div>", unsafe_allow_html=True)
            tags = "".join(f"<span class='skill-tag-red'>{s}</span>" for s in gaps.get("missing_skills", []))
            st.markdown(tags or "<span style='color:#6b7280'>None</span>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='section-header'>Recommendations</div>", unsafe_allow_html=True)
            for rec in gaps.get("recommendations", []):
                st.markdown(f"<div style='color:#9ca3af;font-size:0.85rem;padding:4px 0;border-bottom:1px solid #2d2f3e'>→ {rec}</div>", unsafe_allow_html=True)

        # Interview section
        st.markdown("<div class='section-header' style='margin-top:2rem'>AI Interview</div>", unsafe_allow_html=True)

        if not st.session_state.interview_done:
            idx = st.session_state.current_q
            if idx < len(questions):
                q = questions[idx]
                progress_pct = int((idx / len(questions)) * 100)
                st.progress(progress_pct, f"Question {idx+1} of {len(questions)}")
                st.markdown(f"""
                <div style='background:#1a1d27;border:1px solid #2d2f3e;border-left:3px solid #667eea;border-radius:12px;padding:20px;margin:1rem 0'>
                    <div style='font-size:0.75rem;color:#667eea;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px'>
                        {q.get('type','').upper()} · {q.get('topic','')}
                    </div>
                    <div style='font-size:1.05rem;color:#f9fafb;font-weight:500'>{q.get('question','')}</div>
                </div>
                """, unsafe_allow_html=True)

                answer = st.text_area("Your answer:", key=f"ans_{idx}", height=120, label_visibility="collapsed",
                                      placeholder="Type your answer here...")
                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button("Submit →", type="primary"):
                        if answer.strip():
                            with st.spinner("Evaluating..."):
                                resp = requests.post(f"{API_URL}/evaluate",
                                    json={"question": q, "answer": answer}, timeout=60)
                                st.session_state.evaluations.append(resp.json())
                                st.session_state.current_q += 1
                                st.rerun()
                with col2:
                    if st.button("Skip question"):
                        st.session_state.current_q += 1
                        st.rerun()
            else:
                st.session_state.interview_done = True
                st.rerun()

        if st.session_state.interview_done and st.session_state.evaluations:
            evaluations = st.session_state.evaluations
            avg = round(sum(e["score"] for e in evaluations) / len(evaluations), 1)
            overall = round((fit * 0.6 + avg * 10 * 0.4), 1)

            st.markdown("<div class='section-header'>Final Report</div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            for col, val, label in [
                (col1, f"{fit}/100", "Fit Score"),
                (col2, f"{avg}/10", "Interview Score"),
                (col3, f"{overall}/100", "Overall Score")
            ]:
                col.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{label}</div></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if overall >= 70:
                st.markdown("<div class='decision-hire'>✓ HIRE</div>", unsafe_allow_html=True)
            elif overall >= 50:
                st.markdown("<div class='decision-maybe'>⚡ MAYBE — Further Review Recommended</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='decision-nohire'>✗ NO HIRE</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-header' style='margin-top:2rem'>Interview Transcript</div>", unsafe_allow_html=True)
            for e in evaluations:
                score = e.get("score", 0)
                color = "#10b981" if score >= 7 else "#f59e0b" if score >= 5 else "#ef4444"
                with st.expander(f"Q{e.get('question_id','?')}  ·  Score: {score}/10"):
                    st.markdown(f"**Question:** {e.get('question','')}")
                    st.markdown(f"**Feedback:** {e.get('feedback','')}")
                    if e.get("covered_points"):
                        st.markdown(f"<span class='skill-tag-green'>✓ {' · '.join(e['covered_points'])}</span>", unsafe_allow_html=True)
                    if e.get("missed_points"):
                        st.markdown(f"<span class='skill-tag-red'>✗ {' · '.join(e['missed_points'])}</span>", unsafe_allow_html=True)

            # PDF download
            st.markdown("<div class='section-header' style='margin-top:1.5rem'>Export Report</div>", unsafe_allow_html=True)
            if st.button("📄  Generate PDF Report", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    payload = {
                        "candidate_name": resume.get("candidate_name"),
                        "job_title": jd.get("job_title"),
                        "email": resume.get("email", ""),
                        "experience_years": str(resume.get("experience_years", "")),
                        "education": resume.get("education", ""),
                        "fit_score": fit,
                        "interview_score": avg,
                        "overall_score": overall,
                        "decision": "HIRE" if overall >= 70 else "MAYBE" if overall >= 50 else "NO HIRE",
                        "reason": "Based on fit score and interview performance.",
                        "matched_skills": match.get("matched_skills", []),
                        "missing_skills": gaps.get("missing_skills", []),
                        "weak_areas": gaps.get("weak_areas", []),
                        "recommendations": gaps.get("recommendations", []),
                        "evaluations": evaluations
                    }
                    try:
                        resp = requests.post(f"{API_URL}/generate-report", json=payload, timeout=30)
                        if resp.status_code == 200:
                            st.download_button(
                                "⬇️  Download PDF",
                                data=resp.content,
                                file_name=f"HireGen_{resume.get('candidate_name','Report').replace(' ','_')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Error: {e}")

            if st.button("🔄  Start New Analysis", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

# ============================================================
# PAGE 2: COMPARE CANDIDATES
# ============================================================
elif "Compare" in page:
    st.markdown("# 📊 Candidate Comparison")
    st.markdown("<div style='color:#6b7280;margin-bottom:2rem'>Rank multiple candidates against one job description</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<div class='section-header'>Job Description</div>", unsafe_allow_html=True)
        jd_file = st.file_uploader("", type=["pdf", "txt"], key="cmp_jd", label_visibility="collapsed")
    with col2:
        st.markdown("<div class='section-header'>Resumes (select multiple)</div>", unsafe_allow_html=True)
        resume_files = st.file_uploader("", type=["pdf", "txt"], accept_multiple_files=True, key="cmp_resumes", label_visibility="collapsed")

    if jd_file and resume_files:
        st.info(f"✅ {len(resume_files)} resume(s) ready")
        if st.button("🚀  Compare All Candidates", use_container_width=True):
            with st.spinner(f"Analyzing {len(resume_files)} candidates..."):
                files = [("jd_file", (jd_file.name, jd_file.getvalue()))]
                for rf in resume_files:
                    files.append(("resume_files", (rf.name, rf.getvalue())))
                try:
                    response = requests.post(f"{API_URL}/analyze-multiple", files=files, timeout=600)
                    if response.status_code == 200:
                        data = response.json()
                        rankings = data.get("rankings", [])
                        jd = data.get("jd", {})

                        st.markdown(f"### Rankings for: {jd.get('job_title')}")
                        if rankings:
                            top = rankings[0]
                            st.markdown(f"""
                            <div style='background:linear-gradient(135deg,#052e16,#065f46);border:1px solid #10b981;border-radius:12px;padding:16px;margin-bottom:1rem'>
                                <span style='font-size:0.75rem;color:#10b981;font-weight:600;text-transform:uppercase;letter-spacing:0.1em'>Best Match</span>
                                <div style='font-size:1.2rem;font-weight:700;color:#f9fafb;margin-top:4px'>🥇 {top['candidate_name']} — {top['fit_score']}/100</div>
                            </div>""", unsafe_allow_html=True)

                        for r in rankings:
                            medal = ["🥇","🥈","🥉"][r["rank"]-1] if r["rank"] <= 3 else f"#{r['rank']}"
                            with st.expander(f"{medal}  {r['candidate_name']}  ·  Fit Score: {r['fit_score']} / 100"):
                                col1, col2, col3 = st.columns(3)
                                col1.markdown(f"<div class='metric-card'><div class='metric-value'>{r['fit_score']}</div><div class='metric-label'>Fit Score</div></div>", unsafe_allow_html=True)
                                col2.markdown(f"<div class='metric-card'><div class='metric-value'>{r['total_matched']}/{r['total_required']}</div><div class='metric-label'>Skills Matched</div></div>", unsafe_allow_html=True)
                                col3.markdown(f"<div class='metric-card'><div class='metric-value'>{r['semantic_score']}</div><div class='metric-label'>Semantic Score</div></div>", unsafe_allow_html=True)
                                st.markdown("<br>", unsafe_allow_html=True)
                                matched = "".join(f"<span class='skill-tag-green'>{s}</span>" for s in r.get("matched_skills",[]))
                                missing = "".join(f"<span class='skill-tag-red'>{s}</span>" for s in r.get("gaps",{}).get("missing_skills",[]))
                                st.markdown(f"**Matched:** {matched}", unsafe_allow_html=True)
                                st.markdown(f"**Missing:** {missing}", unsafe_allow_html=True)
                                st.markdown(f"<div style='color:#9ca3af;font-size:0.85rem;margin-top:8px'>{r['resume_data'].get('summary','')}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# ============================================================
# PAGE 3: CHATBOT
# ============================================================
elif "Chatbot" in page:
    st.markdown("# 💬 Recruiter Chatbot")
    st.markdown("<div style='color:#6b7280;margin-bottom:2rem'>Ask anything about your analyzed candidates</div>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if not st.session_state.chat_history:
        st.markdown("<div class='section-header'>Suggested Questions</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        for col, q in [
            (col1, "Who is the best candidate?"),
            (col2, "Who has the strongest Python skills?"),
            (col3, "Who has the most experience?")
        ]:
            if col.button(q, use_container_width=True):
                st.session_state.pending_question = q
                st.rerun()

    if "pending_question" in st.session_state:
        question = st.session_state.pop("pending_question")
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.spinner("Thinking..."):
            resp = requests.post(f"{API_URL}/chat",
                json={"question": question, "history": st.session_state.chat_history}, timeout=60)
            answer = resp.json().get("answer", "Sorry, I could not answer that.")
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if question := st.chat_input("Ask about your candidates..."):
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                resp = requests.post(f"{API_URL}/chat",
                    json={"question": question, "history": st.session_state.chat_history}, timeout=60)
                answer = resp.json().get("answer", "Sorry.")
                st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})

    if st.session_state.chat_history:
        if st.button("🗑️  Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# ============================================================
# PAGE 4: VOICE INTERVIEW
# ============================================================
elif "Voice" in page:
    st.markdown("# 🎤 Voice AI Interview")
    st.markdown("<div style='color:#6b7280;margin-bottom:2rem'>Speak your answers — Whisper transcribes, AI evaluates</div>", unsafe_allow_html=True)

    if st.session_state.voice_step == "upload":
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("<div class='section-header'>Job Description</div>", unsafe_allow_html=True)
            jd_file = st.file_uploader("", type=["pdf","txt"], key="v_jd", label_visibility="collapsed")
        with col2:
            st.markdown("<div class='section-header'>Resume</div>", unsafe_allow_html=True)
            resume_file = st.file_uploader("", type=["pdf","txt"], key="v_resume", label_visibility="collapsed")
        if jd_file and resume_file:
            if st.button("🎤  Prepare Voice Interview", use_container_width=True):
                with st.spinner("Preparing..."):
                    files = {"jd_file": (jd_file.name, jd_file.getvalue()),
                             "resume_file": (resume_file.name, resume_file.getvalue())}
                    resp = requests.post(f"{API_URL}/analyze", files=files, timeout=300)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.voice_result = data
                        st.session_state.voice_questions = data.get("questions", [])
                        st.session_state.voice_step = "interview"
                        st.rerun()

    elif st.session_state.voice_step == "interview":
        questions = st.session_state.voice_questions
        idx = st.session_state.voice_q_idx
        if idx < len(questions):
            q = questions[idx]
            st.progress(int(idx/len(questions)*100), f"Question {idx+1} of {len(questions)}")
            st.markdown(f"""
            <div style='background:#1a1d27;border:1px solid #2d2f3e;border-left:3px solid #667eea;border-radius:12px;padding:20px;margin:1rem 0'>
                <div style='font-size:0.75rem;color:#667eea;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px'>{q.get('type','').upper()} · {q.get('topic','')}</div>
                <div style='font-size:1.05rem;color:#f9fafb;font-weight:500'>{q.get('question','')}</div>
            </div>""", unsafe_allow_html=True)

            audio_file = st.file_uploader("Upload voice answer (.wav/.mp3/.m4a)", type=["wav","mp3","m4a","ogg"], key=f"audio_{idx}")
            typed = st.text_input("Or type your answer:", key=f"typed_{idx}", placeholder="Type here if no audio...")

            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                if audio_file and st.button("🎯  Transcribe & Evaluate", type="primary"):
                    with st.spinner("Transcribing with Whisper..."):
                        resp = requests.post(f"{API_URL}/transcribe", files={"audio_file": (audio_file.name, audio_file.getvalue())}, timeout=60)
                        transcribed = resp.json().get("text", "")
                    if transcribed:
                        st.success(f"Transcribed: _{transcribed}_")
                        with st.spinner("Evaluating..."):
                            ev = requests.post(f"{API_URL}/evaluate", json={"question": q, "answer": transcribed}, timeout=60).json()
                            ev["transcribed_answer"] = transcribed
                            st.session_state.voice_evals.append(ev)
                        st.session_state.voice_q_idx += 1
                        st.rerun()
            with col2:
                if typed and st.button("Submit Typed"):
                    with st.spinner("Evaluating..."):
                        ev = requests.post(f"{API_URL}/evaluate", json={"question": q, "answer": typed}, timeout=60).json()
                        ev["transcribed_answer"] = typed
                        st.session_state.voice_evals.append(ev)
                    st.session_state.voice_q_idx += 1
                    st.rerun()
            with col3:
                if st.button("Skip ⏭"):
                    st.session_state.voice_q_idx += 1
                    st.rerun()
        else:
            st.session_state.voice_step = "report"
            st.rerun()

    elif st.session_state.voice_step == "report":
        evals = st.session_state.voice_evals
        result = st.session_state.voice_result or {}
        match = result.get("match", {})
        resume = result.get("resume", {})
        fit = match.get("fit_score", 0)
        avg = round(sum(e["score"] for e in evals)/len(evals), 1) if evals else 0
        overall = round((fit*0.6 + avg*10*0.4), 1)

        st.markdown(f"### {resume.get('candidate_name','Candidate')} — Voice Interview Report")
        col1, col2, col3 = st.columns(3)
        for col, val, label in [(col1, f"{fit}/100","Fit Score"),(col2, f"{avg}/10","Interview"),(col3, f"{overall}/100","Overall")]:
            col.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{label}</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if overall >= 70: st.markdown("<div class='decision-hire'>✓ HIRE</div>", unsafe_allow_html=True)
        elif overall >= 50: st.markdown("<div class='decision-maybe'>⚡ MAYBE</div>", unsafe_allow_html=True)
        else: st.markdown("<div class='decision-nohire'>✗ NO HIRE</div>", unsafe_allow_html=True)

        for e in evals:
            with st.expander(f"Q{e.get('question_id','?')} · Score: {e['score']}/10"):
                st.markdown(f"**Answer:** _{e.get('transcribed_answer','')}_")
                st.markdown(f"**Feedback:** {e.get('feedback','')}")

        if st.button("🔄  New Voice Interview", use_container_width=True):
            for k in ["voice_step","voice_result","voice_questions","voice_q_idx","voice_evals"]:
                if k in st.session_state: del st.session_state[k]
            st.rerun()