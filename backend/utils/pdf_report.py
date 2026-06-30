from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime

def generate_pdf_report(report_data: dict, output_path: str = "data/hiring_report.pdf") -> str:
    os.makedirs("data", exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "Title", parent=styles["Title"],
        fontSize=24, textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6, alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        fontSize=12, textColor=colors.HexColor("#4a4a8a"),
        spaceAfter=4, alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        "Heading", parent=styles["Heading2"],
        fontSize=14, textColor=colors.HexColor("#1a1a2e"),
        spaceBefore=12, spaceAfter=6,
        borderPad=4
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=11, textColor=colors.HexColor("#333333"),
        spaceAfter=4, leading=16
    )
    decision_hire = ParagraphStyle(
        "DecisionHire", parent=styles["Normal"],
        fontSize=18, textColor=colors.white,
        alignment=TA_CENTER, fontName="Helvetica-Bold"
    )

    content = []

    # Header
    content.append(Paragraph("🤖 HireGen AI", title_style))
    content.append(Paragraph("Automated Hiring Report", subtitle_style))
    content.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}",
        ParagraphStyle("Date", parent=styles["Normal"], fontSize=10,
                      textColor=colors.gray, alignment=TA_CENTER)
    ))
    content.append(Spacer(1, 0.5*cm))
    content.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4a4a8a")))
    content.append(Spacer(1, 0.5*cm))

    # Candidate Info
    content.append(Paragraph("Candidate Overview", heading_style))
    info_data = [
        ["Candidate", report_data.get("candidate_name", "N/A")],
        ["Role Applied", report_data.get("job_title", "N/A")],
        ["Email", report_data.get("email", "N/A")],
        ["Experience", report_data.get("experience_years", "N/A") + " years"],
        ["Education", report_data.get("education", "N/A")],
    ]
    info_table = Table(info_data, colWidths=[5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef0fb")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1a1a2e")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
    ]))
    content.append(info_table)
    content.append(Spacer(1, 0.4*cm))

    # Scores
    content.append(Paragraph("Evaluation Scores", heading_style))
    score_data = [
        ["Metric", "Score", "Rating"],
        ["Fit Score", f"{report_data.get('fit_score', 0)} / 100",
         "⭐ Excellent" if report_data.get("fit_score", 0) >= 70 else "⚠️ Average" if report_data.get("fit_score", 0) >= 50 else "❌ Poor"],
        ["Interview Score", f"{report_data.get('interview_score', 0)} / 10",
         "⭐ Excellent" if report_data.get("interview_score", 0) >= 7 else "⚠️ Average" if report_data.get("interview_score", 0) >= 5 else "❌ Poor"],
        ["Overall Score", f"{report_data.get('overall_score', 0)} / 100",
         "⭐ Excellent" if report_data.get("overall_score", 0) >= 70 else "⚠️ Average" if report_data.get("overall_score", 0) >= 50 else "❌ Poor"],
    ]
    score_table = Table(score_data, colWidths=[7*cm, 4*cm, 6*cm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (1, 1), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ]))
    content.append(score_table)
    content.append(Spacer(1, 0.4*cm))

    # Skills
    content.append(Paragraph("Skills Analysis", heading_style))
    matched = ", ".join(report_data.get("matched_skills", [])) or "None"
    missing = ", ".join(report_data.get("missing_skills", [])) or "None"
    weak = ", ".join(report_data.get("weak_areas", [])) or "None"

    skills_data = [
        ["✅ Matched Skills", matched],
        ["❌ Missing Skills", missing],
        ["⚠️ Weak Areas", weak],
    ]
    skills_table = Table(skills_data, colWidths=[5*cm, 12*cm])
    skills_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#d4edda")),
        ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#f8d7da")),
        ("BACKGROUND", (0, 2), (0, 2), colors.HexColor("#fff3cd")),
    ]))
    content.append(skills_table)
    content.append(Spacer(1, 0.4*cm))

    # Recommendations
    content.append(Paragraph("Recommendations", heading_style))
    for rec in report_data.get("recommendations", []):
        content.append(Paragraph(f"• {rec}", body_style))
    content.append(Spacer(1, 0.4*cm))

    # Interview evaluations
    if report_data.get("evaluations"):
        content.append(Paragraph("Interview Performance", heading_style))
        for e in report_data["evaluations"]:
            q_text = f"Q{e.get('question_id', '')}: {e.get('question', '')}"
            content.append(Paragraph(q_text, ParagraphStyle(
                "Q", parent=styles["Normal"], fontSize=10,
                textColor=colors.HexColor("#1a1a2e"), fontName="Helvetica-Bold",
                spaceBefore=8
            )))
            content.append(Paragraph(
                f"Score: {e.get('score', 0)}/10 — {e.get('feedback', '')}",
                body_style
            ))
        content.append(Spacer(1, 0.4*cm))

    # Final Decision
    content.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4a4a8a")))
    content.append(Spacer(1, 0.3*cm))
    content.append(Paragraph("Final Decision", heading_style))

    decision = report_data.get("decision", "NO HIRE")
    dec_color = colors.HexColor("#28a745") if "HIRE" in decision and "NO" not in decision \
        else colors.HexColor("#ffc107") if "MAYBE" in decision \
        else colors.HexColor("#dc3545")

    decision_table = Table([[Paragraph(decision, decision_hire)]], colWidths=[17*cm])
    decision_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), dec_color),
        ("PADDING", (0, 0), (-1, -1), 16),
        ("ROUNDEDCORNERS", [8]),
    ]))
    content.append(decision_table)
    content.append(Spacer(1, 0.3*cm))
    content.append(Paragraph(
        report_data.get("reason", ""),
        ParagraphStyle("Reason", parent=styles["Normal"], fontSize=11,
                      textColor=colors.HexColor("#555555"), alignment=TA_CENTER)
    ))

    # Footer
    content.append(Spacer(1, 1*cm))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    content.append(Paragraph(
        "Generated by HireGen AI — Multi-Agent Recruitment Copilot",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=9,
                      textColor=colors.gray, alignment=TA_CENTER)
    ))

    doc.build(content)
    return output_path