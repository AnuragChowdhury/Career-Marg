"""
Streamlit Page 4: Personalized Interview Question Generator
"""

import streamlit as st

from utils.helpers import init_session_state, apply_custom_style
from services.interview_service import InterviewService

st.set_page_config(page_title="Interview Prep - Career मार्ग", page_icon="💡", layout="wide")
init_session_state(st.session_state)
apply_custom_style(active_page="interview_prep")

st.title("💡 Personalized Interview Question Generator")
st.caption("Custom candidate questions tailored specifically to your resume, projects, tech stack, and target role gaps")
st.divider()

if not st.session_state.candidate_profile:
    st.warning("⚠️ No resume loaded. Please upload your resume on **1_Resume_Analysis** first.")
    st.stop()

target_role = st.session_state.target_job_role or "Machine Learning Engineer"
missing = st.session_state.skill_gap_result.missing_skills if st.session_state.skill_gap_result else ["Docker", "MLOps"]

st.info(f"🎯 Target Job Role: **{target_role}**")

if st.button("✨ Generate Personalized Question Set", type="primary"):
    with st.spinner("Analyzing resume content, projects, and target role to craft non-generic questions..."):
        int_service = InterviewService()
        questions = int_service.generate_personalized_questions(
            candidate_profile=st.session_state.candidate_profile,
            target_role=target_role,
            missing_skills=missing
        )
        st.session_state.interview_questions = questions
        st.success(f"✓ Generated {len(questions)} personalized questions across 6 categories!")

if not st.session_state.interview_questions:
    st.info("👇 Click the **'Generate Personalized Question Set'** button above to craft custom interview questions tailored specifically to your resume facts.")

# Display Generated Questions by Category
if st.session_state.interview_questions:
    st.divider()
    
    categories = ["Technical", "Project-Based", "Resume-Based", "Behavioral", "HR", "Skill-Gap"]
    
    for cat in categories:
        cat_q = [q for q in st.session_state.interview_questions if q.category == cat]
        if cat_q:
            st.subheader(f"📌 {cat} Questions")
            for q in cat_q:
                with st.expander(f"Question: {q.question}"):
                    st.markdown(f"**Rationale:** {q.rationale}")
                    st.markdown("**Ideal Answer Key Hints:**")
                    for hint in q.ideal_answer_hints:
                        st.write(f"  • 💡 {hint}")
