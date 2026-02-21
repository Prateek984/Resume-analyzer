import streamlit as st
from services.file_reader import extract_text
from core.resume_parser import parse_resume
from core.jd_parser import parse_jd
from core.analyzer import analyze_candidate
from core.report_builder import build_report
from services.usage_tracker import get_user_id, has_used_free, mark_used
from services.pdf_generator import report_to_pdf

st.set_page_config(page_title="Resume Shortlist Checker", layout="centered")

st.title("📄 Resume Shortlist Checker")
st.caption("Know why recruiters skip your resume before applying")

# Inputs
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
st.caption("Tip: After editing your resume, upload again to check improvement")
jd_text = st.text_area("Paste Job Description", height=200)

# Analyze
if st.button("Analyze Resume"):
    if not resume_file or not jd_text:
        st.warning("Upload resume and paste job description")
        st.stop()

    with st.spinner("Analyzing..."):
        resume_text = extract_text(resume_file)
        candidate = parse_resume(resume_text)
        job = parse_jd(jd_text)
        analysis = analyze_candidate(candidate, job)

    st.session_state.previous_analysis = st.session_state.get("analysis")
    st.session_state.analysis = analysis


# Show teaser
if "analysis" in st.session_state:

    analysis = st.session_state.analysis
    score = analysis.get("ats_score", 0)

    st.divider()
    st.subheader("Screening Result")

    if score >= 85:
        st.success("Strong match — you should get interview calls")
    elif score >= 70:
        st.warning("You qualify but recruiters may skip you")
    else:
        st.error("High chance of rejection")

    st.metric("Match Score", f"{score}/100")

    # Show top fix preview
    edits = analysis.get("resume_edits", [])
    if edits:
        st.info("Preview Fix:")
        st.code(edits[0].get("rewrite_example", ""), language="markdown")

    st.write("Unlock full recruiter review below")

    # user_id = get_user_id()

    # if not has_used_free(user_id):
    #     if st.button("Unlock Full Report (Free)"):
    #         st.session_state.show_report = True
    #         mark_used(user_id)
    # else:
    #     st.warning("Free report already used. Payment required to unlock.")
    if st.button("Show Full Report"):
        st.session_state.show_report = True

# Full report UI
if st.session_state.get("show_report"):

    analysis = st.session_state.analysis

    st.divider()
    st.header("Full Resume Review")

    # Copy paste section (most important)
    st.subheader("⭐ Add These Lines To Your Resume")

    edits = analysis.get("resume_edits", [])
    if edits:
        for edit in edits:
            st.code(edit.get("rewrite_example", ""), language="markdown")

    # Priority fixes
    with st.expander("High Impact Fixes"):
        for s in analysis.get("suggestions", []):
            st.write("•", s)

    # Weaknesses
    with st.expander("Why Recruiters Skip You"):
        for w in analysis.get("weaknesses", []):
            st.write("•", w)

    # Strengths
    with st.expander("What Works In Your Resume"):
        for s in analysis.get("strengths", []):
            st.write("•", s)

    # Raw full report (optional)
    with st.expander("Detailed Report"):
        report = build_report(analysis)
        st.text(report)

        pdf_bytes = report_to_pdf(report)

        st.download_button(
            label="📥 Download Report as PDF",
            data=pdf_bytes,
            file_name="resume_review.pdf",
            mime="application/pdf"
        )
    
    # Improvement tracking
if st.session_state.get("previous_analysis"):

    old_score = st.session_state.previous_analysis.get("ats_score", 0)
    new_score = st.session_state.analysis.get("ats_score", 0)
    diff = new_score - old_score

    st.divider()
    st.subheader("📈 Improvement Check")

    if diff > 0:
        st.success(f"Your resume improved by {diff} points!")
    elif diff < 0:
        st.error(f"Score decreased by {abs(diff)} points")
    else:
        st.info("No change detected")
        st.write(f"Previous Score: {old_score}/100")
        st.write(f"Current Score: {new_score}/100")