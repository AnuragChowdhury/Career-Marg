"""
Streamlit Page 8: Professional Profile & Branding Asset Generator
"""

import streamlit as st

from utils.helpers import init_session_state, apply_custom_style
from services.profile_service import ProfileService

st.set_page_config(page_title="Profile Generator - Career मार्ग", page_icon="✨", layout="wide")
init_session_state(st.session_state)
apply_custom_style(active_page="profile_generator")

st.title("✨ Professional Profile & Branding Generator")
st.caption("Generate grounded LinkedIn headlines, bios, portfolio sections, and summaries rooted strictly in your resume facts")
st.divider()

if not st.session_state.candidate_profile:
    st.warning("⚠️ No resume loaded. Please upload your resume on **1_Resume_Analysis** first.")
    st.stop()

st.info("🔒 **Strict Grounding Enforcement**: All generated branding text is directly derived from verified facts in your candidate profile — no fabricated achievements or unearned titles.")

target_role = st.session_state.target_job_role or "Machine Learning Engineer"

if st.button("🚀 Generate Grounded Profile Content", type="primary"):
    with st.spinner("Synthesizing grounded professional branding materials..."):
        prof_svc = ProfileService()
        res = prof_svc.generate_professional_profile(
            candidate_profile=st.session_state.candidate_profile,
            target_role=target_role
        )
        st.session_state.profile_generated = res
        st.success("✓ Professional branding content generated!")

if not st.session_state.profile_generated:
    st.info("👇 Click the **'Generate Grounded Profile Content'** button above to generate professional summaries, LinkedIn headlines, bios, and portfolio descriptions.")

# Render Content Sections
if st.session_state.profile_generated:
    prof = st.session_state.profile_generated

    # Constrain width for optimal readability
    c_pad_left, c_main, c_pad_right = st.columns([0.2, 9.6, 0.2])

    with c_main:
        t1, t2, t3, t4, t5, t6 = st.tabs([
            "📄 Summary",
            "💼 Headline",
            "📝 LinkedIn About",
            "🌐 Portfolio About",
            "👤 Bio",
            "👨‍💻 GitHub README"
        ])

        with t1:
            st.markdown("#### 📄 **Tailored Resume Professional Summary**")
            st.text_area("Summary", value=prof.professional_summary, height=160, key="txt_summary", label_visibility="collapsed")

        with t2:
            st.markdown("#### 💼 **LinkedIn Headline**")
            st.text_area("Headline", value=prof.linkedin_headline, height=100, key="txt_headline", label_visibility="collapsed")

        with t3:
            st.markdown("#### 📝 **LinkedIn About Section**")
            st.text_area("LinkedIn About", value=prof.linkedin_about, height=220, key="txt_linkedin_about", label_visibility="collapsed")

        with t4:
            st.markdown("#### 🌐 **Portfolio Web Page About Section**")
            st.text_area("Portfolio About", value=prof.portfolio_about, height=200, key="txt_portfolio_about", label_visibility="collapsed")

        with t5:
            st.markdown("#### 👤 **Short Professional Bio**")
            st.text_area("Bio", value=prof.professional_bio, height=140, key="txt_bio", label_visibility="collapsed")

        with t6:
            st.markdown("#### 👨‍💻 **GitHub Bio / README Header**")
            st.text_area("GitHub Bio", value=prof.github_description, height=160, key="txt_github", label_visibility="collapsed")
