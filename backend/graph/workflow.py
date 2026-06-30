from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from backend.agents.jd_agent import extract_jd
from backend.agents.resume_agent import extract_resume
from backend.agents.matcher_agent import calculate_fit_score
from backend.agents.skill_gap_agent import identify_skill_gaps
from backend.agents.interview_agent import generate_questions
from backend.agents.evaluator_agent import run_interview

# Define the shared state across all agents
class HireGenState(TypedDict):
    jd_path: str
    resume_path: str
    jd_data: dict
    resume_data: dict
    match_result: dict
    gap_result: dict
    questions: list
    evaluations: list
    final_report: dict

# --- Agent nodes ---

def jd_node(state: HireGenState) -> HireGenState:
    print("\n[1/6] Extracting job description...")
    state["jd_data"] = extract_jd(state["jd_path"])
    return state

def resume_node(state: HireGenState) -> HireGenState:
    print("[2/6] Extracting resume...")
    state["resume_data"] = extract_resume(state["resume_path"])
    return state

def match_node(state: HireGenState) -> HireGenState:
    print("[3/6] Calculating fit score...")
    state["match_result"] = calculate_fit_score(state["jd_data"], state["resume_data"])
    return state

def gap_node(state: HireGenState) -> HireGenState:
    print("[4/6] Identifying skill gaps...")
    state["gap_result"] = identify_skill_gaps(
        state["jd_data"], state["resume_data"], state["match_result"]
    )
    return state

def interview_node(state: HireGenState) -> HireGenState:
    print("[5/6] Generating interview questions...")
    interview = generate_questions(
        state["jd_data"], state["resume_data"], state["gap_result"]
    )
    state["questions"] = interview.get("questions", [])
    state["evaluations"] = run_interview(state["questions"])
    return state

def report_node(state: HireGenState) -> HireGenState:
    print("[6/6] Generating final hiring report...")
    evaluations = state["evaluations"]
    match = state["match_result"]
    gaps = state["gap_result"]
    resume = state["resume_data"]
    jd = state["jd_data"]

    avg_interview = round(
        sum(e["score"] for e in evaluations) / len(evaluations), 1
    ) if evaluations else 0

    fit = match.get("fit_score", 0)
    interview_score = avg_interview * 10
    overall = round((fit * 0.6) + (interview_score * 0.4), 1)

    if overall >= 70:
        decision = "HIRE"
        reason = "Candidate meets the requirements and performed well in the interview."
    elif overall >= 50:
        decision = "MAYBE"
        reason = "Candidate shows potential but has skill gaps that need attention."
    else:
        decision = "NO HIRE"
        reason = "Candidate does not meet the minimum requirements for this role."

    state["final_report"] = {
        "candidate_name": resume.get("candidate_name"),
        "job_title": jd.get("job_title"),
        "fit_score": fit,
        "interview_score": avg_interview,
        "overall_score": overall,
        "matched_skills": match.get("matched_skills", []),
        "missing_skills": gaps.get("missing_skills", []),
        "recommendations": gaps.get("recommendations", []),
        "decision": decision,
        "reason": reason,
        "questions_answered": len(evaluations),
        "total_questions": len(state["questions"])
    }
    return state

# --- Build the graph ---

def build_workflow():
    graph = StateGraph(HireGenState)

    graph.add_node("jd_agent", jd_node)
    graph.add_node("resume_agent", resume_node)
    graph.add_node("match_agent", match_node)
    graph.add_node("gap_agent", gap_node)
    graph.add_node("interview_agent", interview_node)
    graph.add_node("report_agent", report_node)

    graph.set_entry_point("jd_agent")
    graph.add_edge("jd_agent", "resume_agent")
    graph.add_edge("resume_agent", "match_agent")
    graph.add_edge("match_agent", "gap_agent")
    graph.add_edge("gap_agent", "interview_agent")
    graph.add_edge("interview_agent", "report_agent")
    graph.add_edge("report_agent", END)

    return graph.compile()