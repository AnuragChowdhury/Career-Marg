"""
Streamlit Page 3: Skill Gap Analysis & Personalized Learning Roadmap
"""

import streamlit as st

from utils.helpers import init_session_state, apply_custom_style
from services.skill_gap_service import SkillGapService

st.set_page_config(page_title="Skill Gap Analysis - Career मार्ग", page_icon="📊", layout="wide")
init_session_state(st.session_state)
apply_custom_style(active_page="skill_gap")

st.title("📊 Skill Gap Analysis & Learning Roadmap")
st.caption("Identify competence gaps and build a structured, prioritized learning plan")
st.divider()

if not st.session_state.candidate_profile:
    st.warning("⚠️ No resume loaded. Please upload your resume on **1_Resume_Analysis** first.")
    st.stop()

# Target Role Check
target_role = st.session_state.target_job_role or "Machine Learning Engineer"
jd_text = st.session_state.job_description

st.info(f"🎯 Analyzing skill gaps for Target Role: **{target_role}**")

if st.button("🔄 Generate Skill Gap & Roadmap", type="primary") or not st.session_state.skill_gap_result:
    with st.spinner("Comparing candidate competencies against target requirements..."):
        sg_service = SkillGapService()
        sg_res = sg_service.analyze_skill_gaps(
            candidate_profile=st.session_state.candidate_profile,
            target_role=target_role,
            job_description=jd_text
        )
        st.session_state.skill_gap_result = sg_res

        # Save to DB
        try:
            from data.database import save_job_analysis
            ats_score = st.session_state.ats_result.overall_score if st.session_state.ats_result else 0.0
            ats_dict = st.session_state.ats_result.dict() if st.session_state.ats_result else {}
            save_job_analysis(
                candidate_id=st.session_state.candidate_id,
                target_role=target_role,
                job_description=jd_text,
                ats_score=ats_score,
                ats_result_dict=ats_dict,
                skill_gap_dict=sg_res.dict()
            )
        except Exception:
            pass

# Display Categorization Grid
if st.session_state.skill_gap_result:
    res = st.session_state.skill_gap_result

    # 30-Day Skill Gap Action Plan Summary Digest
    sg_service = SkillGapService()
    action_plan = sg_service.generate_30_day_action_plan(res, target_role)

    st.subheader("📅 Executive 30-Day Skill Gap Action Plan")
    st.info(f"💡 **Executive Strategy:** {action_plan['summary_digest']}")

    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.markdown(f"#### 🚀 {action_plan['phase1']['title']}")
        st.write(f"**Focus Skills:** {', '.join(action_plan['phase1']['focus_skills'])}")
        st.caption(action_plan['phase1']['action'])

    with p_col2:
        st.markdown(f"#### ⚙️ {action_plan['phase2']['title']}")
        st.write(f"**Focus Skills:** {', '.join(action_plan['phase2']['focus_skills'])}")
        st.caption(action_plan['phase2']['action'])

    with p_col3:
        st.markdown(f"#### 🛠️ {action_plan['phase3']['title']}")
        st.write(f"**Focus Skills:** {', '.join(action_plan['phase3']['focus_skills'])}")
        st.caption(action_plan['phase3']['action'])

    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("#### ✅ **Strong Match**")
        for s in res.strong_match:
            st.success(f"• {s}")
        if not res.strong_match:
            st.caption("No strong direct skill matches identified yet.")

    with c2:
        st.markdown("#### ⚡ **Partial Match**")
        for s in res.partial_match:
            st.warning(f"• {s}")
        if not res.partial_match:
            st.caption("No partial skill matches.")

    with c3:
        st.markdown("#### ❌ **Missing Skills**")
        for s in res.missing_skills:
            st.error(f"• {s}")
        if not res.missing_skills:
            st.caption("No missing skills identified!")

    with c4:
        st.markdown("#### ➕ **Additional Skills**")
        for s in res.additional_skills:
            st.info(f"• {s}")

    st.divider()

    # Personalized Learning Roadmap Section
    st.subheader("🗺️ Personalized Learning Roadmap")
    st.caption("Prioritized action items to bridge identified technical gaps")

    for item in res.roadmap:
        prio_color = "🔴" if item.priority == "High" else ("🟡" if item.priority == "Medium" else "🟢")
        
        with st.expander(f"{prio_color} **{item.skill}** (Priority: {item.priority})"):
            col_left, col_right = st.columns([1, 1])
            with col_left:
                st.markdown(f"**Why Required:** {item.reason}")
                st.markdown(f"**Importance:** {item.importance}")
                st.markdown("**Topics to Master:**")
                for top in item.topics:
                    st.write(f"  • {top}")
            with col_right:
                st.markdown("**Suggested Resources:**")
                for res_link in item.suggested_resources:
                    st.write(f"  • 📚 {res_link}")
                st.markdown("**Suggested Hands-on Project:**")
                st.success(f"🛠️ {item.suggested_project}")
