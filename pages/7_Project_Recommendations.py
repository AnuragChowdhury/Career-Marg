"""
Streamlit Page 7: Portfolio Project Recommendations Engine
"""

import streamlit as st

from utils.helpers import init_session_state, apply_custom_style
from services.recommendation_service import RecommendationService

st.set_page_config(page_title="Project Recommendations - Career मार्ग", page_icon="🛠️", layout="wide")
init_session_state(st.session_state)
apply_custom_style(active_page="project_recommendations")

st.title("🛠️ Portfolio Project Recommendations")
st.caption("Custom project ideas designed specifically to close skill gaps and maximize employer appeal")
st.divider()

if not st.session_state.candidate_profile:
    st.warning("⚠️ No resume loaded. Please upload your resume on **1_Resume_Analysis** first.")
    st.stop()

target_role = st.session_state.target_job_role or "Machine Learning Engineer"
missing_skills = st.session_state.skill_gap_result.missing_skills if st.session_state.skill_gap_result else ["Docker", "MLOps", "FastAPI"]

st.info(f"🎯 Tailoring project ideas for **{target_role}** addressing missing skills: **{', '.join(missing_skills[:4])}**")

if st.button("✨ Generate Custom Project Recommendations", type="primary"):
    with st.spinner("Synthesizing project architectures based on skill gaps..."):
        rec_svc = RecommendationService()
        projects = rec_svc.generate_project_recommendations(
            candidate_profile=st.session_state.candidate_profile,
            target_role=target_role,
            missing_skills=missing_skills
        )
        st.session_state.project_recommendations = projects
        st.success(f"✓ Recommended {len(projects)} tailored portfolio projects!")

if not st.session_state.project_recommendations:
    st.info("👇 Click the **'Generate Custom Project Recommendations'** button above to generate targeted portfolio projects addressing your skill gaps.")

# Render Recommended Projects
if st.session_state.project_recommendations:
    st.divider()
    
    for idx, proj in enumerate(st.session_state.project_recommendations, 1):
        diff_badge = "🟢 Beginner" if proj.difficulty == "Beginner" else ("🟡 Intermediate" if proj.difficulty == "Intermediate" else "🔴 Advanced")
        
        with st.expander(f"Project #{idx}: {proj.title} ({diff_badge})"):
            st.markdown(f"**Problem Statement:** {proj.problem_statement}")
            
            p1, p2 = st.columns(2)
            with p1:
                st.markdown("**Skills Covered from Identified Skill Gap:**")
                for s in proj.gap_skills_covered:
                    st.error(f"  • {s}")
                st.markdown("**Complete Technology Stack:**")
                st.write(", ".join([f"`{t}`" for t in proj.tech_stack]))
            with p2:
                st.markdown("**Why This Project Improves Employability:**")
                st.success(f"💡 {proj.employability_reason}")
