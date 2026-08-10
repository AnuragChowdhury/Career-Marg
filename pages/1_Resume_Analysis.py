"""
Streamlit Page 1: Resume Upload, Mistral OCR 3 Processing & Candidate Profile Extraction
"""

import streamlit as st
import os
import json

from utils.helpers import validate_uploaded_file, init_session_state, reset_session_state, apply_custom_style, ACTIVE_CANDIDATE_FILE
from services.mistral_ocr_service import MistralOCRService
from services.document_service import DocumentService
from services.resume_parser import ResumeParser
from data.database import save_candidate_profile

st.set_page_config(page_title="Resume Upload & Analysis - Career मार्ग", page_icon="📄", layout="wide")
init_session_state(st.session_state)
apply_custom_style(active_page="resume")

col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("📄 Resume Upload & Multimodal Understanding")
    st.caption("Supports Digital PDFs, Scanned PDFs, DOCX, TXT files, and Image Resumes (JPG, JPEG, PNG) or Direct Text Paste")
with col_head2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Start New Session", type="secondary"):
        reset_session_state(st.session_state)
        st.toast("Session reset cleanly!", icon="🧹")
        st.rerun()

st.divider()

# Input Section (File Upload + Direct Text Area)
input_tab1, input_tab2 = st.tabs(["📁 Upload Resume File (PDF, DOCX, TXT, Image)", "📝 Paste Resume Text"])

file_bytes = None
filename = None
raw_pasted_text = None

with input_tab1:
    uploaded_file = st.file_uploader(
        "Choose a resume file to analyze",
        type=["pdf", "docx", "txt", "jpg", "jpeg", "png"],
        help="Upload your resume in PDF, DOCX, TXT, or image format."
    )
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name

with input_tab2:
    st.markdown("#### **Paste Resume Text Directly**")
    pasted_text = st.text_area(
        "Paste your complete resume text here:",
        height=250,
        placeholder="Paste your raw resume text, work history, skills, and background here...",
        key="resume_text_area"
    )
    if pasted_text.strip():
        raw_pasted_text = pasted_text.strip()
        filename = "pasted_resume.txt"
        file_bytes = raw_pasted_text.encode("utf-8")

if file_bytes is not None and filename is not None:
    file_size = len(file_bytes)

    # 1. File Validation
    is_valid, err_msg = validate_uploaded_file(filename, file_size)
    if not is_valid:
        st.error(f"❌ Validation Error: {err_msg}")
    else:
        if raw_pasted_text:
            st.success(f"✓ Direct text input detected ({len(raw_pasted_text)} characters)")
        else:
            st.success(f"✓ File '{filename}' uploaded successfully ({file_size / 1024:.1f} KB)")
        
        if st.button("🚀 Process & Analyze Resume", type="primary"):
            with st.spinner("Processing document layout & executive understanding..."):
                # 2. Document Extraction & OCR Processing
                ocr_service = MistralOCRService()
                ocr_res = ocr_service.process_document(file_bytes, filename)
                
                raw_text = ocr_res.get("text", "")
                st.session_state.raw_ocr_text = raw_text

                # 3. Document Layout Analysis
                doc_service = DocumentService()
                doc_analysis = doc_service.analyze_layout(file_bytes, filename, raw_text)
                st.session_state.document_analysis = doc_analysis

                # 4. Structured Candidate Profile Parsing
                parser = ResumeParser()
                candidate_profile = parser.parse_resume(raw_text, doc_analysis)
                st.session_state.candidate_profile = candidate_profile
                st.session_state["session_reset"] = False

                # 5. Database Persistence
                try:
                    c_id = save_candidate_profile(
                        filename=filename,
                        file_type=doc_analysis.file_type,
                        raw_text=raw_text,
                        profile_dict=candidate_profile.dict(),
                        doc_analysis_dict=doc_analysis.dict()
                    )
                    st.session_state.candidate_id = c_id
                    try:
                        # Set cid in URL query params — this persists across st.rerun()
                        st.query_params["cid"] = str(c_id)
                    except Exception:
                        pass
                    try:
                        with open(ACTIVE_CANDIDATE_FILE, "w") as f:
                            f.write(str(c_id))
                    except Exception:
                        pass
                except Exception:
                    pass

                # Flag to show success toasts after rerun
                st.session_state["_resume_just_processed"] = True

            # Force rerun so navbar re-renders with ?cid= embedded in all nav links
            # Without this, the navbar shows links WITHOUT ?cid= because it rendered
            # before the candidate ID was set, causing "No resume loaded" on every other page.
            st.rerun()

# Show success toasts after rerun (set by the processing block above)
if st.session_state.pop("_resume_just_processed", False):
    st.toast("🔍 Layout analysis complete!", icon="👀")
    st.toast("🧬 Executive profile parsed successfully!", icon="👤")
    st.toast("✅ Candidate database synchronized!", icon="💾")
    st.success("🎉 Resume analysis complete! You can now navigate to any page using the top navbar.")



# Render Results if Candidate Profile is Loaded
if st.session_state.candidate_profile:
    st.divider()
    profile = st.session_state.candidate_profile
    doc_ana = profile.document_analysis

    st.subheader(f"👤 Candidate Profile: {profile.personal_information.name or 'Extracted Resume'}")

    # Layout Metrics Grid
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Document Type", doc_ana.file_type)
    m2.metric("Page Count", doc_ana.page_count)
    m3.metric("Layout Quality", f"{doc_ana.layout_quality}%")
    m4.metric("Readability Score", f"{doc_ana.readability_score}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Document Structure Warnings
    if doc_ana.formatting_warnings:
        st.markdown("#### ⚠️ **Document Structure & Formatting Insights**")
        for warn in doc_ana.formatting_warnings:
            st.warning(f"• {warn}")

    st.divider()

    # Tabs for Structured Data Views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Extracted Profile",
        "🔍 Document OCR Text",
        "💡 Facts vs AI Suggestions",
        "⚙️ Structured JSON",
        "🛠️ Raw Document Analysis"
    ])

    with tab1:
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("#### **Personal Information**")
            p_info = profile.personal_information
            st.write(f"**Name:** {p_info.name or 'N/A'}")
            st.write(f"**Email:** {p_info.email or 'N/A'}")
            st.write(f"**Phone:** {p_info.phone or 'N/A'}")
            st.write(f"**LinkedIn:** {p_info.linkedin or 'N/A'}")
            st.write(f"**GitHub:** {p_info.github or 'N/A'}")

            st.markdown("#### **Professional Summary**")
            st.write(profile.professional_summary or "N/A")

            st.markdown("#### **Education**")
            for edu in profile.education:
                st.write(f"• **{edu.degree}** — {edu.institution} ({edu.start_date} - {edu.end_date})")

        with col_right:
            st.markdown("#### **Technical Skills**")
            st.write(", ".join([f"`{s}`" for s in profile.technical_skills]) or "None extracted")

            st.markdown("#### **Soft Skills**")
            st.write(", ".join([f"`{s}`" for s in profile.soft_skills]) or "None extracted")

            st.markdown("#### **Projects**")
            for proj in profile.projects:
                st.write(f"• **{proj.title}**: {proj.description}")
                if proj.technologies_used:
                    st.caption(f"Technologies: {', '.join(proj.technologies_used)}")

            st.markdown("#### **Work Experience**")
            for exp in profile.work_experience:
                st.write(f"• **{exp.job_title}** at {exp.company}")
                for b in exp.bullet_points:
                    st.caption(f"  - {b}")

    with tab2:
        st.markdown("#### **Raw Extracted OCR Text (Mistral OCR 3)**")
        st.text_area("OCR Markdown Text", st.session_state.raw_ocr_text, height=350)

    with tab3:
        col_f, col_r = st.columns(2)
        with col_f:
            st.markdown("#### ✅ **Facts Explicitly Found in Resume**")
            for fact in profile.extracted_facts:
                st.success(f"• {fact}")
        with col_r:
            st.markdown("#### 💡 **AI Recommendations & Improvements**")
            for rec in profile.ai_recommendations:
                st.info(f"• {rec}")

    with tab4:
        st.markdown("#### **Parsed JSON Schema**")
        st.json(profile.dict())

    with tab5:
        st.markdown("#### **Document Layout Metadata**")
        st.json(doc_ana.dict())
