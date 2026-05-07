import streamlit as st
import os
from dotenv import load_dotenv

from pdf_parser import get_resume_text
from analyzer import analyze_resume, get_keyword_match
from utils import (is_resume_text, extract_score_from_text,
                   get_score_color, get_strength_label, word_count)

load_dotenv()

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# custom styling
st.markdown("""
<style>
    .score-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 10px;
        border-left: 4px solid #4f8ef7;
    }
    .score-card.red   { border-left-color: #e05252; }
    .score-card.orange { border-left-color: #f0a500; }
    .score-card.green { border-left-color: #3dba6e; }
    .section-box {
        background-color: #1a1d2e;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 14px;
    }
    .big-score {
        font-size: 48px;
        font-weight: bold;
        color: #ffffff;
    }
    .sub-score { font-size: 13px; color: #7a8099; }
</style>
""", unsafe_allow_html=True)


# ---- SIDEBAR ----
with st.sidebar:
    st.header("How it works")
    st.markdown("""
    1. Upload your resume PDF
    2. Select your target role
    3. Click Analyze
    4. Get a detailed honest report
    """)
    st.markdown("---")
    st.markdown("**Powered by:** Google Gemini 1.5 Flash")
    st.markdown("**Note:** Your resume is not stored anywhere.")
    if not os.getenv("GEMINI_API_KEY"):
        st.warning("⚠️ GEMINI_API_KEY not found in .env")
    else:
        st.success("✅ API key configured")


# ---- HEADER ----
st.title("📄 AI Resume Analyzer")
st.markdown(
    "Get an honest, recruiter-level analysis of your resume. No fake praise.")
st.markdown("---")


# ---- INPUTS ----
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"]
    )

with col2:
    target_role = st.selectbox(
        "Select your target role",
        ["ML Engineer", "Data Analyst", "Data Engineer",
         "Backend Developer", "Software Engineer",
         "DevOps Engineer", "Frontend Developer", "Full Stack Developer"]
    )
    show_keywords = st.checkbox("Also run keyword match analysis", value=True)

analyze_btn = st.button("🔍 Analyze My Resume",
                        use_container_width=True, type="primary")
st.markdown("---")


# ---- HELPER FUNCTIONS ----
def parse_analysis_sections(text):
    """Split Gemini's response into a dict keyed by section headers."""
    sections = {}
    current_section = None
    current_content = []

    for line in text.splitlines():
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line.replace("## ", "").strip()
            current_content = []
        else:
            if current_section:
                current_content.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def display_section(title, content):
    """Render a styled section box if content exists."""
    if not content or not content.strip():
        return
    st.subheader(title)
    st.markdown(f"""
    <div class="section-box">
        {content.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)


# ---- MAIN ANALYSIS FLOW ----
if analyze_btn:
    if uploaded_file is None:
        st.error("Please upload your resume PDF first.")
        st.stop()

    with st.spinner("Reading your resume..."):
        resume_text = get_resume_text(uploaded_file)

    is_valid, msg = is_resume_text(resume_text)
    if not is_valid:
        st.error(msg)
        st.stop()

    # quick stats
    c1, c2, c3 = st.columns(3)
    c1.metric("Words extracted", word_count(resume_text))
    c2.metric("Characters", len(resume_text))
    c3.metric("Target role", target_role)
    st.markdown("---")

    # keyword match
    keyword_result = None
    if show_keywords:
        with st.spinner("Checking keyword match..."):
            keyword_result = get_keyword_match(resume_text, target_role)

    # main analysis
    with st.spinner("Analyzing your resume... this takes 15-30 seconds..."):
        analysis = analyze_resume(resume_text, target_role)

    if "Error" in analysis:
        st.error(f"Analysis failed: {analysis}")
        st.stop()

    st.success("Analysis complete!")

    # score cards
    overall_score = extract_score_from_text(analysis, "Overall Score")
    ats_score = extract_score_from_text(analysis, "ATS Score")
    recruiter_score = extract_score_from_text(analysis, "Recruiter Impression")

    sc1, sc2, sc3, sc4 = st.columns(4)

    with sc1:
        color = get_score_color(overall_score)
        st.markdown(f"""
        <div class="score-card {color}">
            <div class="sub-score">Overall Score</div>
            <div class="big-score">{overall_score if overall_score else "?"}<span style="font-size:20px;color:#7a8099">/100</span></div>
        </div>""", unsafe_allow_html=True)

    with sc2:
        color = get_score_color(ats_score)
        st.markdown(f"""
        <div class="score-card {color}">
            <div class="sub-score">ATS Score</div>
            <div class="big-score">{ats_score if ats_score else "?"}<span style="font-size:20px;color:#7a8099">/100</span></div>
        </div>""", unsafe_allow_html=True)

    with sc3:
        color = get_score_color(recruiter_score)
        st.markdown(f"""
        <div class="score-card {color}">
            <div class="sub-score">Recruiter Impression</div>
            <div class="big-score">{recruiter_score if recruiter_score else "?"}<span style="font-size:20px;color:#7a8099">/100</span></div>
        </div>""", unsafe_allow_html=True)

    with sc4:
        label = get_strength_label(overall_score)
        st.markdown(f"""
        <div class="score-card">
            <div class="sub-score">Resume Strength</div>
            <div style="font-size:22px;font-weight:bold;color:#fff;margin-top:8px">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # keyword match display
    if keyword_result:
        st.subheader("🔑 Keyword Match Analysis")
        match_pct = extract_score_from_text(keyword_result, "Keyword Match")
        if match_pct:
            st.progress(match_pct / 100)
            st.markdown(
                f"**{match_pct}% keyword match** with {target_role} job descriptions")
        with st.expander("See keyword details"):
            st.markdown(keyword_result)

    # analysis sections
    sections = parse_analysis_sections(analysis)

    display_section("👤 Candidate Summary",
                    sections.get("CANDIDATE SUMMARY", ""))
    display_section("🚨 Biggest Problems",
                    sections.get("BIGGEST PROBLEMS", ""))
    display_section("🤖 ATS Issues",
                    sections.get("ATS ISSUES", ""))
    display_section("⚙️ Technical Skills Analysis",
                    sections.get("TECHNICAL SKILLS ANALYSIS", ""))
    display_section("🗂️ Project Review",
                    sections.get("PROJECT REVIEW", ""))
    display_section("💼 Experience Analysis",
                    sections.get("EXPERIENCE ANALYSIS", ""))
    display_section("✏️ Bullet Point Improvements",
                    sections.get("BULLET POINT IMPROVEMENTS", ""))
    display_section(f"🔍 Missing Keywords for {target_role}",
                    sections.get(f"MISSING KEYWORDS FOR {target_role.upper()}", ""))
    display_section("👔 Recruiter Perspective",
                    sections.get("RECRUITER PERSPECTIVE", ""))
    display_section("📊 Hiring Chances",
                    sections.get("HIRING CHANCES", ""))
    display_section("🗺️ Improvement Roadmap",
                    sections.get("IMPROVEMENT ROADMAP", ""))

    st.markdown("---")

    # download report
    report_text = f"RESUME ANALYSIS REPORT\nTarget Role: {target_role}\n\n{analysis}"
    st.download_button(
        label="📥 Download Full Report",
        data=report_text,
        file_name=f"resume_analysis_{target_role.replace(' ', '_').lower()}.txt",
        mime="text/plain"
    )

    with st.expander("📋 View raw analysis"):
        st.markdown(analysis)
