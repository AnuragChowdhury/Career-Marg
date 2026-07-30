"""
Streamlit Page 2: ATS Compatibility Optimization & Bullet Point Refinement
"""

import streamlit as st
import plotly.graph_objects as go

from utils.helpers import init_session_state, apply_custom_style
from services.ats_service import ATSService
from data.database import save_job_analysis

st.set_page_config(page_title="ATS Optimization - Career मार्ग", page_icon="🎯", layout="wide")
init_session_state(st.session_state)
apply_custom_style(active_page="ats")

st.title("🎯 ATS Compatibility Optimization")
st.caption("Transparent 5-factor scoring & keyword match against target Job Descriptions")
st.divider()

# Disclaimer Alert
st.info("ℹ️ **Disclaimer**: The ATS score generated is an analytical estimate based on standard industry Applicant Tracking System parsing algorithms. It is not an official score from any specific employer.")

if not st.session_state.candidate_profile:
    st.warning("⚠️ No resume loaded. Please upload your resume on **1_Resume_Analysis** first.")
    st.stop()

# Inputs
col_in1, col_in2 = st.columns([1, 1.5])

with col_in1:
    target_role_input = st.text_input(
        "Target Job Title / Role",
        value=st.session_state.target_job_role or "Machine Learning Engineer",
        placeholder="e.g. Data Scientist, Full Stack Developer"
    )

with col_in2:
    jd_input = st.text_area(
        "Target Job Description (Paste full text or key requirements)",
        value=st.session_state.job_description,
        placeholder="Paste job description text here...",
        height=120
    )

if st.button("⚡ Run ATS Compatibility Analysis", type="primary"):
    st.session_state.target_job_role = target_role_input
    st.session_state.job_description = jd_input

    with st.spinner("Analyzing keyword density, skill overlap, and layout compliance..."):
        ats_service = ATSService()
        ats_res = ats_service.analyze_ats_compatibility(
            candidate_profile=st.session_state.candidate_profile,
            target_role=target_role_input,
            job_description=jd_input
        )
        st.session_state.ats_result = ats_res

        # Save to DB
        try:
            save_job_analysis(
                candidate_id=st.session_state.candidate_id,
                target_role=target_role_input,
                job_description=jd_input,
                ats_score=ats_res.overall_score,
                ats_result_dict=ats_res.dict(),
                skill_gap_dict={}
            )
        except Exception:
            pass

        st.success("✓ ATS Analysis Completed!")

# Render Results if ATS Result exists
if st.session_state.ats_result:
    st.divider()
    res = st.session_state.ats_result
    factors = res.factor_scores

    # Score Gauge & Factors Grid
    c_gauge, c_factors = st.columns([1, 1.3])

    with c_gauge:
        st.markdown("#### **Overall Estimated ATS Score**")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=res.overall_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "ATS Score (0 - 100)", 'font': {'color': '#1E293B', 'size': 16, 'family': 'Inter, sans-serif'}},
            number={'font': {'color': '#0F172A', 'size': 42, 'family': 'Inter, sans-serif'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#64748B', 'tickfont': {'color': '#475569', 'size': 12}},
                'bar': {'color': "#FF5C00"},
                'steps': [
                    {'range': [0, 50], 'color': "#FEE2E2"},
                    {'range': [50, 75], 'color': "#FEF3C7"},
                    {'range': [75, 100], 'color': "#DCFCE7"}
                ]
            }
        ))
        fig.update_layout(
            height=280, 
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#1E293B', 'family': 'Inter, sans-serif'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with c_factors:
        st.markdown("#### **Transparent Sub-Factor Scoring Methodology**")
        f1, f2 = st.columns(2)
        f1.metric("Required Skill Match (40%)", f"{factors.required_skill_match}%")
        f1.metric("Keyword Overlap (25%)", f"{factors.keyword_match}%")
        f1.metric("Structure Quality (10%)", f"{factors.structure_quality}%")

        f2.metric("Experience Relevance (15%)", f"{factors.experience_relevance}%")
        f2.metric("Education Relevance (10%)", f"{factors.education_relevance}%")

    st.divider()

    # Detailed Match Breakdown Tabs
    tab_k, tab_s, tab_a, tab_imp = st.tabs([
        "🔑 Keywords Analysis",
        "🛠️ Skills Matching",
        "📌 Experience & Education Alignment",
        "✍️ Resume Bullet Improvements"
    ])

    with tab_k:
        k_matched, k_missing = st.columns(2)
        with k_matched:
            st.markdown("#### ✅ **Matching Keywords Found**")
            st.write(", ".join([f"`{k}`" for k in res.matching_keywords]) or "None")
        with k_missing:
            st.markdown("#### ❌ **Missing Keywords in Resume**")
            st.write(", ".join([f"`{k}`" for k in res.missing_keywords]) or "None")

    with tab_s:
        s_found, s_missing = st.columns(2)
        with s_found:
            st.markdown("#### ✅ **Relevant Skills Found**")
            for s in res.relevant_skills_found:
                st.success(f"• {s}")
        with s_missing:
            st.markdown("#### ⚠️ **Required Skills Missing**")
            for s in res.required_skills_missing:
                st.error(f"• {s}")

    with tab_a:
        st.markdown("#### **Alignment Summaries**")
        st.info(f"**Experience Alignment:** {res.experience_alignment}")
        st.info(f"**Education Alignment:** {res.education_alignment}")
        st.info(f"**Certifications Alignment:** {res.certification_alignment}")

        if res.formatting_issues:
            st.markdown("#### **Formatting Issues**")
            for issue in res.formatting_issues:
                st.warning(f"• {issue}")

    with tab_imp:
        st.markdown("#### ✍️ **AI Resume Bullet Point Improvement Suggestions**")
        st.caption("Transform basic bullets into quantifiable, action-verb driven achievements without fabricating data.")

        ats_svc = ATSService()
        improvements = ats_svc.suggest_resume_improvements(st.session_state.candidate_profile)

        for idx, imp in enumerate(improvements, 1):
            with st.expander(f"Bullet Suggestion #{idx}: {imp.original_bullet[:60]}..."):
                st.markdown("**Original:**")
                st.code(imp.original_bullet)
                st.markdown("**Suggested Version:**")
                st.success(imp.suggested_bullet)
                st.caption(f"💡 **Reason:** {imp.reason}")
                if imp.placeholder_note:
                    st.warning(f"📌 {imp.placeholder_note}")
