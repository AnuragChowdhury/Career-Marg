"""
Streamlit Page 6: Career Role Recommendations & Industry Readiness Score
"""

import streamlit as st
import plotly.express as px

from utils.helpers import init_session_state, apply_custom_style
from services.career_service import CareerService

st.set_page_config(page_title="Career Recommendations - Career मार्ग", page_icon="📈", layout="wide")
init_session_state(st.session_state)
apply_custom_style(active_page="career_recommendations")

st.title("📈 Career Recommendations & Industry Readiness")
st.caption("AI-driven role match analysis and comprehensive employability evaluation")
st.divider()

if not st.session_state.candidate_profile:
    st.warning("⚠️ No resume loaded. Please upload your resume on **1_Resume_Analysis** first.")
    st.stop()

career_svc = CareerService()

# 1. Career Role Recommendation Engine
st.subheader("🎯 Career Role Match Recommendations")
recs = career_svc.recommend_career_roles(st.session_state.candidate_profile)
st.session_state.career_recommendations = recs

col_cards = st.columns(len(recs[:3]))
for idx, role in enumerate(recs[:3]):
    with col_cards[idx]:
        st.markdown(f"""
        <div style='background: #FFFFFF; padding: 1.2rem; border-radius: 12px; border: 1px solid #E2E8F0; border-top: 4px solid #FF5C00; box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);'>
            <h3 style='margin:0; font-size: 1.1rem; color: #1E293B; font-weight: 700;'>{role.role_name}</h3>
            <h2 style='color: #FF5C00; margin: 0.4rem 0 0 0; font-size: 1.8rem; font-weight: 800;'>{role.match_percentage}% Match</h2>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 0.6rem;'></div>", unsafe_allow_html=True)
        st.write(f"**Matching Skills:** {', '.join(role.matching_skills[:4])}")
        st.write(f"**Missing Skills:** {', '.join(role.missing_skills[:3]) or 'None'}")

st.markdown("<br>", unsafe_allow_html=True)

# Role Details Expander
with st.expander("🔍 View Full Career Role Alignment Breakdown"):
    for role in recs:
        st.markdown(f"### **{role.role_name}** — Match Score: `{role.match_percentage}%`")
        r1, r2 = st.columns(2)
        with r1:
            st.success(f"**Matching Skills:** {', '.join(role.matching_skills)}")
            st.error(f"**Missing Skills:** {', '.join(role.missing_skills) or 'None'}")
        with r2:
            st.markdown("**Recommended Next Steps:**")
            for step in role.recommended_next_steps:
                st.write(f"  • {step}")
        st.divider()

st.divider()

# 2. Industry Readiness Evaluation (Feature 9)
st.subheader("🛡️ Industry Readiness Score")

ats_score = st.session_state.ats_result.overall_score if st.session_state.ats_result else 75.0
mock_scores = [h.overall_answer_score for h in st.session_state.mock_interview_history]
avg_mock = sum(mock_scores) / len(mock_scores) if mock_scores else 70.0

readiness = career_svc.evaluate_industry_readiness(
    candidate_profile=st.session_state.candidate_profile,
    ats_score=ats_score,
    skill_gap_percentage=25.0,
    mock_interview_score=avg_mock
)
st.session_state.industry_readiness = readiness

m_col1, m_col2 = st.columns([1, 1.3])

with m_col1:
    st.metric("Overall Industry Readiness Score", f"{readiness.overall_score:.1f}%")
    
    # Category Bar Chart
    df_cat = {"Category": list(readiness.category_scores.keys()), "Score": list(readiness.category_scores.values())}
    fig = px.bar(
        df_cat, 
        x="Score", 
        y="Category", 
        orientation="h", 
        title="Category Breakdown (0-100)", 
        color="Score", 
        color_continuous_scale="Oranges",
        template="plotly_white"
    )
    fig.update_layout(
        height=320, 
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1E293B', family='Inter, sans-serif', size=13),
        title_font=dict(color='#0F172A', size=16, family='Inter, sans-serif'),
        xaxis=dict(
            title_font=dict(color='#1E293B', size=13),
            tickfont=dict(color='#334155', size=12),
            gridcolor='#E2E8F0'
        ),
        yaxis=dict(
            title_font=dict(color='#1E293B', size=13),
            tickfont=dict(color='#1E293B', size=13),
            gridcolor='#E2E8F0'
        ),
        coloraxis_colorbar=dict(
            title_font=dict(color='#1E293B', size=12),
            tickfont=dict(color='#334155', size=12)
        )
    )
    st.plotly_chart(fig, use_container_width=True)

with m_col2:
    st.markdown("#### **Readiness Strengths & Improvement Plan**")
    if readiness.strengths:
        st.markdown("**Core Strengths:**")
        for s in readiness.strengths:
            st.success(f"• {s}")

    if readiness.actionable_improvement_plan:
        st.markdown("**Actionable Improvement Plan:**")
        for plan in readiness.actionable_improvement_plan:
            st.warning(f"• {plan}")
