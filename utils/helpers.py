"""
Helper Utilities for Career मार्ग.
File validation, text cleanups, and Streamlit session state management.
"""

import os
import re
from typing import Tuple, List, Dict, Any

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".docx", ".txt"}
MAX_FILE_SIZE_MB = 15.0


def validate_uploaded_file(filename: str, file_size_bytes: int) -> Tuple[bool, str]:
    """
    Validates uploaded resume file extension and size limit.
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file format '{ext}'. Supported formats: PDF, DOCX, TXT, JPG, JPEG, PNG."
    
    size_mb = file_size_bytes / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File size ({size_mb:.2f} MB) exceeds maximum limit of {MAX_FILE_SIZE_MB} MB."
    
    return True, "Valid file"


def clean_text(text: str) -> str:
    """
    Clean raw OCR or document text by normalizing whitespaces and non-printable characters.
    """
    if not text:
        return ""
    # Normalize multiple spaces/newlines
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_skills_from_text(text: str, skill_ontology: List[str]) -> List[str]:
    """
    Extract matching skills from text using exact & regex word boundary matching.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    found_skills = set()
    
    for skill in skill_ontology:
        skill_lower = skill.lower()
        # Escaped pattern for multi-word or special skills like C++ or React.js
        pattern = r'(?:\b|_)' + re.escape(skill_lower) + r'(?:\b|_)'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    return sorted(list(found_skills))


def init_session_state(st_session_state: Any) -> None:
    """
    Initialize Streamlit session state variables if not already set.
    """
    defaults = {
        "candidate_id": None,
        "candidate_profile": None,
        "raw_ocr_text": "",
        "document_analysis": None,
        "target_job_role": "",
        "job_description": "",
        "ats_result": None,
        "skill_gap_result": None,
        "interview_questions": [],
        "mock_interview_history": [],
        "current_question_index": 0,
        "career_recommendations": [],
        "project_recommendations": [],
        "industry_readiness": None,
        "profile_generated": None
    }
    
    for key, value in defaults.items():
        if key not in st_session_state:
            st_session_state[key] = value

    # Auto-load active candidate profile across multi-page navigation or page refreshes
    if st_session_state["candidate_profile"] is None and not st_session_state.get("session_reset", False):
        try:
            from data.database import SessionLocal, CandidateRecord, JobAnalysisRecord, init_db
            from models.schemas import CandidateProfile, DocumentAnalysis, ATSResult, SkillGapResult
            
            init_db()
            db_session = SessionLocal()
            try:
                rec = None
                active_file = os.path.join("data", "active_candidate_id.txt")
                if os.path.exists(active_file):
                    with open(active_file, "r") as f:
                        c_id_str = f.read().strip()
                    if c_id_str and c_id_str.isdigit():
                        c_id = int(c_id_str)
                        rec = db_session.query(CandidateRecord).filter(CandidateRecord.id == c_id).first()
                
                # Fallback: Query the most recently created candidate record from database
                if rec is None:
                    rec = db_session.query(CandidateRecord).order_by(CandidateRecord.id.desc()).first()

                if rec and rec.profile_json:
                    st_session_state["candidate_id"] = rec.id
                    st_session_state["candidate_profile"] = CandidateProfile.parse_raw(rec.profile_json)
                    st_session_state["raw_ocr_text"] = rec.raw_text or ""
                    if rec.doc_analysis_json:
                        st_session_state["document_analysis"] = DocumentAnalysis.parse_raw(rec.doc_analysis_json)
                    
                    # Ensure active_candidate_id.txt is updated
                    try:
                        os.makedirs("data", exist_ok=True)
                        with open(active_file, "w") as f:
                            f.write(str(rec.id))
                    except Exception:
                        pass

                    # Query latest associated job analysis
                    job_rec = db_session.query(JobAnalysisRecord).filter(
                        JobAnalysisRecord.candidate_id == rec.id
                    ).order_by(JobAnalysisRecord.id.desc()).first()
                    
                    if job_rec:
                        if job_rec.target_role:
                            st_session_state["target_job_role"] = job_rec.target_role
                        if job_rec.job_description:
                            st_session_state["job_description"] = job_rec.job_description
                        if job_rec.ats_result_json and job_rec.ats_result_json != "{}":
                            st_session_state["ats_result"] = ATSResult.parse_raw(job_rec.ats_result_json)
                        if job_rec.skill_gap_json and job_rec.skill_gap_json != "{}":
                            st_session_state["skill_gap_result"] = SkillGapResult.parse_raw(job_rec.skill_gap_json)
            finally:
                db_session.close()
        except Exception:
            pass


def reset_session_state(st_session_state: Any) -> None:
    """
    Resets Streamlit session state to default empty values when a new session
    is explicitly started or when no document is uploaded.
    """
    defaults = {
        "candidate_id": None,
        "candidate_profile": None,
        "raw_ocr_text": "",
        "document_analysis": None,
        "target_job_role": "",
        "job_description": "",
        "ats_result": None,
        "skill_gap_result": None,
        "interview_questions": [],
        "mock_interview_history": [],
        "current_question_index": 0,
        "career_recommendations": [],
        "project_recommendations": [],
        "industry_readiness": None,
        "profile_generated": None
    }
    for key, value in defaults.items():
        st_session_state[key] = value

    active_file = os.path.join("data", "active_candidate_id.txt")
    if os.path.exists(active_file):
        try:
            os.remove(active_file)
        except Exception:
            pass


def apply_custom_style(active_page: str = None, hide_sidebar: bool = True) -> None:
    """
    Applies the custom Starlight Platinum Executive theme CSS, hides the sidebar and header globally,
    and renders the sticky top navigation bar.
    """
    import streamlit as st
    
    # Enforce hiding the sidebar and header globally
    st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    [data-testid="stHeader"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

    # Determine background color: white for marketing homepage, off-white for others
    is_marketing = (active_page == "home")
    bg_color = "#FFFFFF" if is_marketing else "#EFF1F3"

    extra_css = ""
    if active_page == "home":
        extra_css = """
    div[data-testid="stImage"] > img {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        border-radius: 0px !important;
        max-height: none !important;
    }
    """

    # Inject main application styling
    st.markdown(f"""
<style>
    /* Enforce Theme Color Overrides for Text Visibility (Supports Dark and Light Browser Modes) */
    :root, .stApp {{
        --text-color: #0F172A !important;
        --title-color: #0F172A !important;
        --header-color: #0F172A !important;
        --body-color: #0F172A !important;
        --background-color: {bg_color} !important;
    }}

    body, .stApp {{
        background-color: {bg_color} !important;
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }}
    .block-container {{
        max-width: 95% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 6.5rem !important; /* Pushes content down below the sticky header navbar */
        padding-bottom: 2.5rem !important;
    }}

    /* Global Container Padding & Typography */
    body {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0F172A;
    }}

    /* Standard Text Elements Overrides */
    .stApp, .stMarkdown p, .stMarkdown li, .stMarkdown span, .stCaptionContainer, h1, h2, h3, h4, h5, h6, label, p, li, td, th {{
        color: #0F172A !important;
    }}
    
    /* Captions/Subtitle grey color override */
    .stMarkdown caption, .stCaptionContainer, [data-testid="stCaptionContainer"], st.caption {{
        color: #475569 !important;
    }}

    /* Inputs & Select Boxes Overrides to remain light with dark text */
    input, textarea, select, button[role="combobox"] {{
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }}
    
    /* Expander elements text override */
    [data-testid="stExpander"] div, .stExpander, div[data-testid="stExpander"] p {{
        color: #0F172A !important;
    }}

    /* Enforce toast text to be white/light to contrast with its dark background */
    [data-testid="stToast"] p, 
    [data-testid="stToast"] span, 
    [data-testid="stToast"] div, 
    [data-testid="stToast"] {{
        color: #FFFFFF !important;
    }}

    /* Floating Tooltip & Popover Light Theme Styling Override */
    div[data-baseweb="tooltip"],
    div[role="tooltip"],
    div[data-testid="stTooltipContent"],
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="tooltip"] > div,
    div[data-testid="stTooltipContent"] > div,
    .stTooltipContent {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.15) !important;
    }}

    div[data-baseweb="tooltip"] p,
    div[data-baseweb="tooltip"] span,
    div[data-baseweb="tooltip"] div,
    div[role="tooltip"] p,
    div[role="tooltip"] span,
    div[role="tooltip"] div,
    div[data-testid="stTooltipContent"] p,
    div[data-testid="stTooltipContent"] span,
    div[data-testid="stTooltipContent"] div,
    div[data-baseweb="popover"] p,
    div[data-baseweb="popover"] span,
    div[data-baseweb="popover"] div,
    .stTooltipContent p,
    .stTooltipContent span,
    .stTooltipContent div {{
        color: #0F172A !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }}

    /* Hero Page Content Styling */
    .hero-main-title {{
        font-size: 4.8rem !important;
        font-weight: 800 !important;
        color: #1A1F36 !important;
        line-height: 1.05 !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -2px !important;
    }}
    .hero-desc-para {{
        font-size: 1.15rem !important;
        color: #475569 !important;
        line-height: 1.6 !important;
        margin-bottom: 2.2rem !important;
        font-weight: 500 !important;
    }}
    .hero-learn-more-btn {{
        background: linear-gradient(135deg, #FF5C00 0%, #D43F00 100%) !important;
        color: #FFFFFF !important;
        border-radius: 30px !important;
        padding: 0.8rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 5px 15px rgba(255, 92, 0, 0.3) !important;
        display: inline-block !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
    }}
    .hero-learn-more-btn:hover {{
        background: linear-gradient(135deg, #FF7A00 0%, #FF5C00 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(255, 92, 0, 0.4) !important;
        color: #FFFFFF !important;
        text-decoration: none !important;
    }}

    /* Pipeline Diagram & Animations */
    .learn-more-details {{
        display: block !important;
        margin-top: 1.5rem !important;
        width: 100% !important;
    }}
    .learn-more-details summary::-webkit-details-marker {{
        display: none !important;
    }}
    .learn-more-details summary {{
        list-style: none !important;
        outline: none !important;
        cursor: pointer !important;
        display: inline-block !important;
    }}
    .learn-more-details[open] .learn-more-content {{
        animation: slideDown 0.4s ease-out forwards !important;
    }}
    
    /* Toggle text inside summary based on details state */
    .btn-text-collapse {{
        display: none !important;
    }}
    .btn-text-expand {{
        display: inline !important;
    }}
    .learn-more-details[open] .btn-text-collapse {{
        display: inline !important;
    }}
    .learn-more-details[open] .btn-text-expand {{
        display: none !important;
    }}
    
    .learn-more-content {{
        margin-top: 1.5rem !important;
        padding: 2rem !important;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 20px !important;
        box-shadow: 0 15px 35px rgba(15, 23, 42, 0.05) !important;
        opacity: 0;
        transform: translateY(-10px);
        box-sizing: border-box !important;
        width: 100% !important;
    }}
    
    @keyframes slideDown {{
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .pipeline-title {{
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        color: #1E293B !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        letter-spacing: -0.4px !important;
    }}

    /* SVG Network Node Graph Styles */
    .graph-container {{
        display: flex !important;
        flex-direction: column !important;
        gap: 1.5rem !important;
        width: 100% !important;
        background: #FFFFFF !important;
        box-sizing: border-box !important;
    }}
    
    .graph-svg-wrapper {{
        width: 100% !important;
        background: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 20px !important;
        padding: 1rem !important;
        box-sizing: border-box !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.01) !important;
    }}

    .bg-path {{
        stroke: #E2E8F0 !important;
        stroke-width: 4 !important;
        fill: none !important;
        stroke-linecap: round !important;
    }}

    .flow-path {{
        stroke: #FF5C00 !important;
        stroke-width: 4 !important;
        fill: none !important;
        stroke-linecap: round !important;
        stroke-dasharray: 8 16 !important;
        stroke-dashoffset: 0 !important;
        animation: flowPulse 4s linear infinite !important;
    }}

    @keyframes flowPulse {{
        to {{
            stroke-dashoffset: -48 !important;
        }}
    }}

    /* Stagger flow animation delays for visual flow paths */
    .flow-top-1 {{ animation-duration: 3s !important; }}
    .flow-bot-1 {{ animation-duration: 3s !important; }}
    .flow-top-2 {{ animation-duration: 2.5s !important; }}
    .flow-bot-2 {{ animation-duration: 2.5s !important; }}
    .flow-top-3 {{ animation-duration: 3s !important; }}
    .flow-bot-3 {{ animation-duration: 3s !important; }}

    .node-group {{
        cursor: pointer !important;
    }}

    .node-circle {{
        fill: #FFFFFF !important;
        stroke: #CBD5E1 !important;
        stroke-width: 3 !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }}

    .node-icon {{
        font-size: 1.25rem !important;
        text-anchor: middle !important;
        pointer-events: none !important;
        user-select: none !important;
    }}

    .node-label {{
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        fill: #64748B !important;
        text-anchor: middle !important;
        pointer-events: none !important;
        user-select: none !important;
        transition: all 0.3s ease !important;
    }}

    /* Node Hover States */
    .node-group:hover .node-circle {{
        fill: #FFEBE0 !important;
        stroke: #FF5C00 !important;
        stroke-width: 4 !important;
        r: 25 !important;
        filter: drop-shadow(0 4px 8px rgba(255, 92, 0, 0.25)) !important;
    }}

    .node-group:hover .node-label {{
        fill: #FF5C00 !important;
        font-weight: 900 !important;
    }}

    /* Details Card Overlays */
    .graph-details-box {{
        position: relative !important;
        width: 100% !important;
        min-height: 120px !important;
    }}

    .detail-card {{
        display: none;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 1.2rem 1.5rem !important;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.04) !important;
        animation: fadeInNode 0.4s ease-out forwards !important;
        box-sizing: border-box !important;
        border-left: 4px solid #FF5C00 !important;
    }}

    @keyframes fadeInNode {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .detail-card h4 {{
        margin: 0 0 0.4rem 0 !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        color: #1E293B !important;
    }}

    .detail-card p {{
        margin: 0 !important;
        font-size: 0.82rem !important;
        color: #64748B !important;
        line-height: 1.5 !important;
    }}

    .detail-card.d-default {{
        display: block;
        border-left-color: #64748B !important;
    }}

    /* Has selectors overlaying nodes details dynamic CSS state */
    .graph-container:has(.n-ingest:hover) .d-default {{ display: none; }}
    .graph-container:has(.n-ingest:hover) .d-ingest {{ display: block; }}

    .graph-container:has(.n-ats:hover) .d-default {{ display: none; }}
    .graph-container:has(.n-ats:hover) .d-ats {{ display: block; }}

    .graph-container:has(.n-skills:hover) .d-default {{ display: none; }}
    .graph-container:has(.n-skills:hover) .d-skills {{ display: block; }}

    .graph-container:has(.n-interview:hover) .d-default {{ display: none; }}
    .graph-container:has(.n-interview:hover) .d-interview {{ display: block; }}

    .graph-container:has(.n-brand:hover) .d-default {{ display: none; }}
    .graph-container:has(.n-brand:hover) .d-brand {{ display: block; }}

    .graph-container:has(.n-success:hover) .d-default {{ display: none; }}
    .graph-container:has(.n-success:hover) .d-success {{ display: block; }}

    .get-started-btn {{
        background: linear-gradient(135deg, #FF5C00 0%, #D43F00 100%) !important;
        color: #FFFFFF !important;
        border-radius: 30px !important;
        padding: 0.75rem 2.2rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 5px 12px rgba(255, 92, 0, 0.25) !important;
        display: inline-block !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
    }}
    .get-started-btn:hover {{
        background: linear-gradient(135deg, #FF7A00 0%, #FF5C00 100%) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 7px 18px rgba(255, 92, 0, 0.3) !important;
        color: #FFFFFF !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
    }}

    /* Card Containers & Typography */
    .dashboard-card {{
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02) !important;
        margin-bottom: 1.2rem !important;
    }}

    /* Style st.container(border=True) to match our SaaS card layout */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 20px !important;
        padding: 1.4rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02) !important;
    }}
    
    .card-title {{
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: #1E293B !important;
        margin-bottom: 0.8rem !important;
        letter-spacing: -0.3px !important;
    }}

    .main-title {{
        font-size: 2.3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #1E293B 0%, #FF5C00 60%, #E63F00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -0.6px;
    }}
    
    .sub-title {{
        font-size: 1.02rem;
        color: #475569;
        margin-bottom: 1.2rem;
        font-weight: 600;
        line-height: 1.5;
    }}

    /* Hero Banner Image Styling */
    div[data-testid="stImage"] > img {{
        max-height: 220px !important;
        object-fit: cover !important;
        object-position: center !important;
        border-radius: 14px !important;
        width: 100% !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 8px 25px rgba(30, 27, 75, 0.08) !important;
    }}
    
    /* Candidate Summary Header layout */
    .candidate-main-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #FF5C00;
        border-radius: 14px;
        padding: 1rem 1.4rem;
        box-shadow: 0 4px 15px rgba(30, 27, 75, 0.02);
        margin-bottom: 1.5rem;
    }}
    
    .candidate-title {{
        font-size: 1.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }}
    
    .badge-chip {{
        display: inline-block;
        padding: 0.32rem 0.8rem;
        border-radius: 20px;
        font-size: 0.83rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-top: 0.4rem;
    }}
    .chip-amber {{ background: #FFFBEB; color: #B45309; border: 1px solid #FDE68A; }}
    .chip-emerald {{ background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }}
    .chip-purple {{ background: #F5F3FF; color: #6D28D9; border: 1px solid #DDD6FE; }}
    
    /* Clean Corporate Metric Cards */
    .metric-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }}
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 92, 0, 0.1);
    }}
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #D43F00, #FF5C00);
    }}
    .metric-card-2::before {{ background: linear-gradient(90deg, #059669, #10B981); }}
    .metric-card-3::before {{ background: linear-gradient(90deg, #FF5C00, #F59E0B); }}
    .metric-card-4::before {{ background: linear-gradient(90deg, #7C3AED, #9333EA); }}

    .metric-title {{
        font-size: 0.82rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.6px;
        margin-bottom: 0.3rem;
    }}
    .metric-value {{
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
    }}

    /* Executive Feature Grid Cards */
    .feature-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.3rem;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
        height: 100%;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .feature-card:hover {{
        border-color: #FF5C00;
        box-shadow: 0 8px 20px rgba(255, 92, 0, 0.08);
    }}
    .feature-card h4 {{
        margin: 0 0 0.4rem 0;
        font-size: 1.02rem;
        font-weight: 700;
        color: #1E293B;
    }}
    .feature-card p {{
        color: #475569;
        font-size: 0.86rem;
        margin: 0;
        line-height: 1.5;
    }}

    /* Custom Component Overrides for all buttons */
    button[data-testid="stBaseButton-secondary"],
    button[data-testid="baseButton-secondary"],
    button[kind="secondary"],
    div[data-testid="stButton"] > button,
    div.stButton > button,
    button[data-baseweb="button"]:not([kind="primary"]) {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
    }}
    
    button[data-testid="stBaseButton-secondary"] *,
    button[data-testid="baseButton-secondary"] *,
    button[kind="secondary"] *,
    div[data-testid="stButton"] > button *,
    div.stButton > button *,
    button[data-baseweb="button"]:not([kind="primary"]) * {{
        color: #0F172A !important;
        fill: #0F172A !important;
    }}
    
    button[data-testid="stBaseButton-secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[kind="secondary"]:hover,
    div[data-testid="stButton"] > button:hover,
    div.stButton > button:hover,
    button[data-baseweb="button"]:not([kind="primary"]):hover {{
        background-color: #FFF8F5 !important;
        background: #FFF8F5 !important;
        color: #FF5C00 !important;
        border-color: #FF5C00 !important;
        box-shadow: 0 4px 12px rgba(255, 92, 0, 0.15) !important;
    }}
    
    button[data-testid="stBaseButton-secondary"]:hover *,
    button[data-testid="baseButton-secondary"]:hover *,
    button[kind="secondary"]:hover *,
    div[data-testid="stButton"] > button:hover *,
    div.stButton > button:hover *,
    button[data-baseweb="button"]:not([kind="primary"]):hover * {{
        color: #FF5C00 !important;
        fill: #FF5C00 !important;
    }}

    /* Primary Buttons (Orange Gradient) */
    button[data-testid="stBaseButton-primary"],
    button[data-testid="baseButton-primary"],
    button[kind="primary"],
    div[data-testid="stButton"] > button[kind="primary"] {{
        background: linear-gradient(135deg, #FF5C00 0%, #D43F00 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(255, 92, 0, 0.25) !important;
        transition: all 0.2s ease !important;
    }}
    
    button[data-testid="stBaseButton-primary"] *,
    button[data-testid="baseButton-primary"] *,
    button[kind="primary"] *,
    div[data-testid="stButton"] > button[kind="primary"] * {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }}
    
    button[data-testid="stBaseButton-primary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    button[kind="primary"]:hover,
    div[data-testid="stButton"] > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #FF7A00 0%, #FF5C00 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 15px rgba(255, 92, 0, 0.35) !important;
        transform: translateY(-1px) !important;
    }}
    
    button[data-testid="stBaseButton-primary"]:hover *,
    button[data-testid="baseButton-primary"]:hover *,
    button[kind="primary"]:hover *,
    div[data-testid="stButton"] > button[kind="primary"]:hover * {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }}



    button[data-baseweb="tab"] {{
        color: #475569 !important;
        font-weight: 600 !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #FF5C00 !important;
        border-bottom-color: #FF5C00 !important;
    }}

    div[data-testid="stProgressBar"] > div > div > div {{
        background-color: #FF5C00 !important;
    }}

    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {{
        border-color: #FF5C00 !important;
        box-shadow: 0 0 0 1px #FF5C00 !important;
    }}

    /* Streamlit File Uploader Custom Light Theme (Matches Reference Screenshot) */
    div[data-testid="stFileUploader"] {{
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.2rem !important;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03) !important;
        border: 1px solid #E2E8F0 !important;
    }}

    div[data-testid="stFileUploader"] label {{
        color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.6rem !important;
    }}

    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {{
        background-color: #F8FAFC !important;
        border: 1px dashed #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 1.2rem 1.5rem !important;
        transition: all 0.2s ease-in-out !important;
    }}

    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:hover {{
        border-color: #FF5C00 !important;
        background-color: #FFF8F5 !important;
    }}

    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] span,
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] p,
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] div {{
        color: #0F172A !important;
    }}

    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] small {{
        color: #64748B !important;
    }}

    /* Orange Cloud Upload Icon */
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] svg {{
        fill: #FF5C00 !important;
        color: #FF5C00 !important;
    }}

    /* Browse files button styling (White bg, Orange border & text) */
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] button {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #FF5C00 !important;
        border: 1px solid #FF5C00 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.45rem 1.2rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    }}

    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] button:hover {{
        background-color: #FF5C00 !important;
        background: #FF5C00 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(255, 92, 0, 0.25) !important;
    }}

    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] button * {{
        color: #FF5C00 !important;
    }}
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] button:hover * {{
        color: #FFFFFF !important;
    }}

    /* Uploaded file item pill */
    div[data-testid="stFileUploaderFileData"],
    div[data-testid="stFileUploaderFile"],
    div[data-testid="stUploadedFileData"],
    ul[data-testid="stFileUploaderUserUploadedFiles"] li,
    div[data-testid="stFileUploader"] ul li,
    [data-testid="stFileUploaderFile"] {{
        background-color: #F8FAFC !important;
        background: #F8FAFC !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }}

    div[data-testid="stFileUploaderFileData"] *,
    div[data-testid="stFileUploaderFile"] *,
    [data-testid="stFileUploaderFileName"] {{
        color: #0F172A !important;
    }}

    button[data-testid="stFileUploaderDeleteBtn"],
    div[data-testid="stFileUploaderFileData"] button {{
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #FF5C00 !important;
        border-radius: 6px !important;
    }}
    button[data-testid="stFileUploaderDeleteBtn"]:hover {{
        background-color: #FFF8F5 !important;
        border-color: #FF5C00 !important;
    }}

    /* Streamlit Expander (st.expander) Light Executive Theme Override */
    div[data-testid="stExpander"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03) !important;
        margin-bottom: 0.8rem !important;
        overflow: hidden !important;
    }}
    div[data-testid="stExpander"] details {{
        background-color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
    }}
    div[data-testid="stExpander"] summary {{
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        font-weight: 700 !important;
        padding: 0.75rem 1rem !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }}
    div[data-testid="stExpander"] summary:hover {{
        background-color: #FFF8F5 !important;
        color: #FF5C00 !important;
    }}
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary p,
    div[data-testid="stExpander"] summary div {{
        color: #1E293B !important;
        font-weight: 700 !important;
    }}
    div[data-testid="stExpander"] summary:hover span,
    div[data-testid="stExpander"] summary:hover p,
    div[data-testid="stExpander"] summary:hover div {{
        color: #FF5C00 !important;
    }}
    div[data-testid="stExpander"] summary svg {{
        fill: #64748B !important;
        color: #64748B !important;
    }}
    div[data-testid="stExpander"] summary:hover svg {{
        fill: #FF5C00 !important;
        color: #FF5C00 !important;
    }}
    div[data-testid="stExpanderDetails"] {{
        background-color: #FFFFFF !important;
        color: #334155 !important;
        padding: 1.2rem !important;
        border-top: 1px solid #F1F5F9 !important;
    }}

    /* Inline Code Chips & Skill Badges Light Executive Theme Override */
    code, .stMarkdown code, div[data-testid="stMarkdownContainer"] code {{
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        padding: 0.2rem 0.55rem !important;
        font-family: 'Fira Code', 'Consolas', 'Courier New', monospace !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
    }}

    /* Custom Top Navigation Bar Styling (Stretched & Pinned to Top) */
    .custom-navbar {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        width: 100% !important;
        min-height: 60px !important;
        z-index: 999999 !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.4rem 2rem;
        background-color: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        box-sizing: border-box !important;
    }}
    .navbar-logo {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        flex-shrink: 0;
    }}
    .logo-emoji {{
        font-size: 1.45rem;
    }}
    .logo-text {{
        font-size: 1.2rem;
        font-weight: 800;
        color: #1E293B;
        letter-spacing: -0.3px;
    }}
    .logo-tag {{
        font-size: 0.75rem;
        background: linear-gradient(135deg, #FF5C00 0%, #D43F00 100%);
        color: white;
        padding: 0.1rem 0.45rem;
        border-radius: 4px;
        font-weight: 700;
        text-transform: uppercase;
    }}
    .navbar-links {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        flex-wrap: wrap;
    }}
    .nav-link {{
        text-decoration: none !important;
        color: #64748B !important;
        font-weight: 600;
        font-size: 0.86rem;
        padding: 0.4rem 0.75rem;
        border-radius: 6px;
        transition: all 0.2s ease;
        white-space: nowrap;
    }}
    .nav-link:hover {{
        color: #FF5C00 !important;
        background-color: #F8FAFC;
    }}
    .active-link {{
        background: linear-gradient(135deg, #FF5C00 0%, #D43F00 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700;
        box-shadow: 0 3px 8px rgba(255, 92, 0, 0.15);
    }}

    /* ========================================================= */
    /* RESPONSIVE MEDIA QUERIES (Mobile, Tablet, Small Laptops)  */
    /* ========================================================= */

    /* Large Tablets & Laptops (<= 1200px) */
    @media (max-width: 1200px) {{
        .custom-navbar {{
            padding: 0.4rem 1.2rem !important;
            flex-wrap: wrap !important;
            gap: 0.4rem !important;
        }}
        .navbar-links {{
            width: 100% !important;
            overflow-x: auto !important;
            white-space: nowrap !important;
            padding-bottom: 0.25rem !important;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none; /* Firefox */
        }}
        .navbar-links::-webkit-scrollbar {{
            display: none; /* Chrome/Safari */
        }}
        .nav-link {{
            font-size: 0.8rem !important;
            padding: 0.35rem 0.6rem !important;
            flex-shrink: 0 !important;
        }}
        .block-container {{
            padding-top: 7.2rem !important;
            padding-left: 1.2rem !important;
            padding-right: 1.2rem !important;
        }}
    }}

    /* Mobile Devices & Small Tablets (<= 768px) */
    @media (max-width: 768px) {{
        .block-container {{
            max-width: 100% !important;
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 7.8rem !important;
            padding-bottom: 1.5rem !important;
        }}

        .hero-main-title {{
            font-size: 2.3rem !important;
            letter-spacing: -0.8px !important;
            margin-bottom: 0.8rem !important;
            line-height: 1.15 !important;
        }}

        .hero-tagline {{
            font-size: 1.1rem !important;
        }}

        .hero-desc-para {{
            font-size: 0.96rem !important;
            margin-bottom: 1.4rem !important;
        }}

        .hero-learn-more-btn, .get-started-btn {{
            padding: 0.65rem 1.5rem !important;
            font-size: 0.9rem !important;
            width: 100% !important;
            text-align: center !important;
            box-sizing: border-box !important;
        }}

        .custom-navbar {{
            padding: 0.4rem 0.85rem !important;
        }}

        .logo-text {{
            font-size: 1.05rem !important;
        }}

        .logo-tag {{
            font-size: 0.68rem !important;
        }}

        /* Streamlit Grid Columns Auto-Stack on Mobile */
        div[data-testid="column"] {{
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }}

        /* Metric Cards Responsiveness */
        .metric-card {{
            padding: 1rem 1.1rem !important;
            margin-bottom: 0.8rem !important;
        }}

        .metric-value {{
            font-size: 1.65rem !important;
        }}

        /* Plotly & SVG Responsiveness */
        .js-plotly-plot, .plotly, div[data-testid="stPlotlyChart"] {{
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: auto !important;
        }}

        /* Data Tables & Code Chips Horizontal Scrolling */
        table, div[data-testid="stTable"] {{
            display: block !important;
            overflow-x: auto !important;
            white-space: nowrap !important;
        }}

        div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {{
            padding: 1.2rem 0.8rem !important;
        }}
    }}

    /* Extra Small Phones (<= 480px) */
    @media (max-width: 480px) {{
        .hero-main-title {{
            font-size: 1.95rem !important;
        }}

        .block-container {{
            padding-top: 8.2rem !important;
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }}

        .nav-link {{
            font-size: 0.76rem !important;
            padding: 0.3rem 0.5rem !important;
        }}
        .medium-story-btn, .medium-story-btn:visited, .medium-story-btn:hover, .medium-story-btn:active {{
            color: #FFFFFF !important;
            text-decoration: none !important;
        }}
    }}
    {extra_css}
</style>
""", unsafe_allow_html=True)

    # Render Navbar if active_page is provided
    if active_page:
        pages = [
            {"label": "Home", "url": "/", "key": "home"},
            {"label": "Resume Parser", "url": "/Resume_Analysis", "key": "resume"},
            {"label": "ATS Auditor", "url": "/ATS_Analysis", "key": "ats"},
            {"label": "Skill Gap", "url": "/Skill_Gap_Analysis", "key": "skill_gap"},
            {"label": "Interview Prep", "url": "/Interview_Preparation", "key": "interview_prep"},
            {"label": "Mock Interview", "url": "/Mock_Interview", "key": "mock_interview"},
            {"label": "Career Match", "url": "/Career_Recommendations", "key": "career_recommendations"},
            {"label": "Portfolio Projects", "url": "/Project_Recommendations", "key": "project_recommendations"},
            {"label": "Profile Suite", "url": "/Profile_Generator", "key": "profile_generator"},
            {"label": "Dashboard", "url": "/SaaS_Dashboard", "key": "saas_dashboard"},
            {"label": "Technical Specs", "url": "/Technical_Architecture", "key": "technical_architecture"},
        ]
        
        links_html = ""
        for p in pages:
            is_active = (p["key"] == active_page)
            active_class = "class='nav-link active-link'" if is_active else "class='nav-link'"
            links_html += f'<a href="{p["url"]}" target="_self" {active_class}>{p["label"]}</a>\n'
        
        medium_url = "https://medium.com/@anuragchowdhury19official/building-career-%E0%A4%AE%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%97-how-i-built-an-executive-multimodal-ai-career-preparation-intelligence-2e85b983ebbd"
        links_html += f'<a href="{medium_url}" target="_blank" class="nav-link" style="color: #FF5C00 !important; font-weight: 700;">📖 Medium Story</a>\n'
            
        import base64
        import os
        logo_path = os.path.join("assets", "logo_icon.png")
        icon_b64 = ""
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                icon_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        navbar_html = f"""<div class="custom-navbar">
<div class="navbar-logo">
<img src="data:image/png;base64,{icon_b64}" width="28" height="28" style="vertical-align: middle; margin-right: 6px;" /> <span class="logo-text">Career मार्ग</span> <span class="logo-tag">Suite</span>
</div>
<div class="navbar-links">
{links_html}
</div>
</div>"""
        st.markdown(navbar_html, unsafe_allow_html=True)
