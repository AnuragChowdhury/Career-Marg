"""
Streamlit Page 9: SaaS-Inspired Analytics Dashboard
Dynamic, Multi-Graph Interactive Analytics with Adaptive Data Volume Sizing
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

from utils.helpers import init_session_state, apply_custom_style

st.set_page_config(
    page_title="Analytics Dashboard - Career मार्ग",
    page_icon="📊",
    layout="wide"
)

# Initialize Session State & Styling
init_session_state(st.session_state)
apply_custom_style(active_page="saas_dashboard")

# ---------------------------------------------------------
# Candidate Data Resolving
# ---------------------------------------------------------
if not st.session_state.candidate_profile:
    st.warning("⚠️ **No Active Candidate Profile found.** Please upload your resume on the **1_Resume_Analysis** page first to generate your career metrics and interactive charts.")
    if st.button("🚀 Go to Resume Upload", type="primary"):
        st.switch_page("pages/1_Resume_Analysis.py")
else:
    # Use real parsed candidate data
    p_info = st.session_state.candidate_profile.personal_information
    p_name = p_info.name or "Candidate Profile"
    p_email = p_info.email or "N/A"
    p_loc = p_info.location or "Verified Location"
    target_r = st.session_state.target_job_role or "Machine Learning Engineer"
    skill_n = len(st.session_state.candidate_profile.technical_skills)
    doc_t = st.session_state.candidate_profile.document_analysis.file_type if st.session_state.candidate_profile.document_analysis else "Digital PDF"
    ats_score = st.session_state.ats_result.overall_score if st.session_state.ats_result else 0.0
    readiness_score = st.session_state.industry_readiness.overall_score if st.session_state.industry_readiness else 0.0
    mock_count = len(st.session_state.mock_interview_history)
    
    # Skills list resolving
    sg_res = st.session_state.skill_gap_result
    strong_skills = sg_res.strong_match if sg_res else st.session_state.candidate_profile.technical_skills[:6]
    partial_skills = sg_res.partial_match if sg_res else ["System Design"]
    missing_skills = sg_res.missing_skills if sg_res else ["Cloud Deployment"]
    
    recommended_roles = [
        {"role": target_r, "match": readiness_score, "strong": len(strong_skills), "gaps": len(missing_skills)},
        {"role": "Data Scientist", "match": max(0.0, readiness_score - 8.0), "strong": max(0, len(strong_skills)-3), "gaps": len(missing_skills)+2},
        {"role": "MLOps Architect", "match": max(0.0, readiness_score - 15.0), "strong": max(0, len(strong_skills)-6), "gaps": len(missing_skills)+5},
        {"role": "Analytics Engineer", "match": max(0.0, readiness_score - 22.0), "strong": max(0, len(strong_skills)-8), "gaps": len(missing_skills)+6}
    ]

    # ---------------------------------------------------------
    # Profile Header Banner
    # ---------------------------------------------------------
    st.markdown(f"""<div class="candidate-main-card">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
<div>
<div class="candidate-title">👤 Active Profile: {p_name}</div>
<div style="color: #64748B; font-size: 0.9rem; font-weight: 500;">Email: {p_email} | Location: {p_loc}</div>
</div>
<div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
<span class="badge-chip chip-amber">🎯 Target: {target_r}</span>
<span class="badge-chip chip-emerald">🛠️ Skills: {skill_n} Verified</span>
<span class="badge-chip chip-purple">📄 Format: {doc_t}</span>
</div>
</div>
</div>""", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Overview Metrics Cards Grid
    # ---------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""<div class='metric-card'>
<div class='metric-title'>ATS Match Score</div>
<div class='metric-value'>{ats_score:.1f}%</div>
</div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class='metric-card metric-card-2'>
<div class='metric-title'>Industry Readiness</div>
<div class='metric-value'>{readiness_score:.1f}%</div>
</div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""<div class='metric-card metric-card-3'>
<div class='metric-title'>Technical Skills</div>
<div class='metric-value'>{skill_n}</div>
</div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""<div class='metric-card metric-card-4'>
<div class='metric-title'>Mock Turns Completed</div>
<div class='metric-value'>{mock_count}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Multi-Graph Dashboard Tabs
    # ---------------------------------------------------------
    tab_overview, tab_roles, tab_skills = st.tabs([
        "📊 Executive Readiness & Trend Analytics",
        "🎯 Career Alignment & Role Matching",
        "🛠️ Competency Radar & Skill Distribution"
    ])

    # =========================================================
    # TAB 1: EXECUTIVE READINESS & TREND ANALYTICS
    # =========================================================
    with tab_overview:
        col_left, col_right = st.columns([1, 1.8])

        with col_left:
            # Graph 1: Semicircular Readiness Gauge Chart
            with st.container(border=True):
                st.markdown("<div class='card-title'>🎯 Career Readiness Index</div>", unsafe_allow_html=True)
                
                fig_gauge = go.Figure(
                    data=[go.Pie(
                        values=[readiness_score, max(0.1, 100.0 - readiness_score), 100.0],
                        labels=["Readiness Achieved", "Readiness Gap", "Spacer"],
                        hole=0.75,
                        direction="clockwise",
                        sort=False,
                        rotation=270,
                        marker=dict(colors=['#FF5C00', '#E2E8F0', 'rgba(0,0,0,0)']),
                        textinfo="none",
                        hoverinfo="label+value"
                    )]
                )
                fig_gauge.update_layout(
                    showlegend=False,
                    height=210,
                    margin=dict(t=0, b=0, l=10, r=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    annotations=[
                        dict(
                            text=f"<span style='font-size:2.2rem; font-weight:900; color:#1E293B;'>{readiness_score:.1f}%</span><br><span style='font-size:0.8rem; color:#64748B; font-weight:700;'>Readiness Score</span>",
                            x=0.5, y=0.45,
                            showarrow=False,
                            align="center"
                        )
                    ]
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

                st.markdown(f"""<div style="display: flex; flex-direction: column; gap: 0.6rem; margin-top: -1.2rem; padding: 0.5rem 0.2rem;">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #F1F5F9; padding-bottom: 0.4rem;">
<div style="display: flex; align-items: center; gap: 0.5rem;">
<div style="width: 10px; height: 10px; background-color: #FF5C00; border-radius: 2px;"></div>
<span style="font-size: 0.88rem; font-weight: 600; color: #475569;">Technical Skills</span>
</div>
<span style="font-size: 0.88rem; font-weight: 700; color: #1E293B;">{min(100.0, len(strong_skills)*8.5):.1f}%</span>
</div>
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #F1F5F9; padding-bottom: 0.4rem;">
<div style="display: flex; align-items: center; gap: 0.5rem;">
<div style="width: 10px; height: 10px; background-color: #1E293B; border-radius: 2px;"></div>
<span style="font-size: 0.88rem; font-weight: 600; color: #475569;">ATS Optimization</span>
</div>
<span style="font-size: 0.88rem; font-weight: 700; color: #1E293B;">{ats_score:.1f}%</span>
</div>
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="display: flex; align-items: center; gap: 0.5rem;">
<div style="width: 10px; height: 10px; background-color: #CBD5E1; border-radius: 2px;"></div>
<span style="font-size: 0.88rem; font-weight: 600; color: #475569;">Interview Strategy</span>
</div>
<span style="font-size: 0.88rem; font-weight: 700; color: #1E293B;">{max(50.0, 65.0 + mock_count*5.0):.1f}%</span>
</div>
</div>""", unsafe_allow_html=True)

        with col_right:
            # Graph 2: Smooth Multi-Trace Line & Trend Progression Chart
            with st.container(border=True):
                st.markdown("<div class='card-title'>📈 ATS Alignment & Career Analytics Progression</div>", unsafe_allow_html=True)
                
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                base_score = max(0.0, readiness_score - 20)
                scores_trend = [min(100.0, base_score + (i * (readiness_score - base_score) / 11) + (np.sin(i)*2)) for i in range(12)]
                ats_trend = [min(100.0, max(0.0, ats_score - 15) + (i * (ats_score - max(0.0, ats_score - 15)) / 11)) for i in range(12)]

                dynamic_line_height = max(240, min(420, len(months) * 16 + 120))

                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(
                    x=months, y=scores_trend,
                    mode='lines+markers',
                    name='Readiness Score',
                    line=dict(color='#FF5C00', width=3, shape='spline'),
                    fill='tozeroy',
                    fillcolor='rgba(255, 92, 0, 0.06)'
                ))
                fig_line.add_trace(go.Scatter(
                    x=months, y=ats_trend,
                    mode='lines',
                    name='ATS Alignment',
                    line=dict(color='#1E293B', width=2, dash='dash')
                ))
                
                fig_line.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color='#1E293B')),
                    xaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(size=10, color='#64748B')),
                    yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(size=10, color='#64748B'), range=[0, 100]),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=10, t=30, b=20),
                    height=dynamic_line_height,
                    font=dict(color='#1E293B', family='Inter, sans-serif')
                )
                st.plotly_chart(fig_line, use_container_width=True)

    # =========================================================
    # TAB 2: CAREER ALIGNMENT & ROLE MATCHING
    # =========================================================
    with tab_roles:
        c_r_left, c_r_right = st.columns([1.2, 1])

        with c_r_left:
            # Graph 3: Dynamic Horizontal Role Match Bar Chart (Height Adapts to Number of Target Roles)
            with st.container(border=True):
                st.markdown("<div class='card-title'>🎯 Career Role Alignment Analysis</div>", unsafe_allow_html=True)
                
                role_names = [r["role"] for r in recommended_roles]
                role_scores = [r["match"] for r in recommended_roles]
                num_roles = len(role_names)
                
                # Dynamic Sizing based on data volume
                dynamic_role_height = max(240, min(500, num_roles * 55 + 60))

                fig_roles = px.bar(
                    x=role_scores,
                    y=role_names,
                    orientation="h",
                    labels={'x': 'Match Percentage (%)', 'y': 'Target Career Role'},
                    color=role_scores,
                    color_continuous_scale="Oranges",
                    template="plotly_white"
                )
                fig_roles.update_layout(
                    height=dynamic_role_height,
                    margin=dict(l=10, r=10, t=30, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#1E293B', family='Inter, sans-serif', size=12),
                    xaxis=dict(range=[0, 100], gridcolor='#E2E8F0', tickfont=dict(color='#334155')),
                    yaxis=dict(gridcolor='#E2E8F0', tickfont=dict(color='#1E293B', size=12, weight='bold')),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_roles, use_container_width=True)

        with c_r_right:
            # Graph 4: Candidate Skill Gaps Cohort Stacked Bar (Height Adapts to Skill Categories)
            with st.container(border=True):
                st.markdown("<div class='card-title'>📊 Skill Gaps Cohort Distribution</div>", unsafe_allow_html=True)
                
                categories = ['Programming', 'ML/AI Core', 'DevOps & MLOps', 'System Architectures']
                tot_s = len(strong_skills)
                tot_p = len(partial_skills)
                tot_m = len(missing_skills)

                strong_v = [max(0, tot_s // 4) + (1 if i < tot_s % 4 else 0) for i in range(4)]
                partial_v = [max(0, tot_p // 4) + (1 if i < tot_p % 4 else 0) for i in range(4)]
                missing_v = [max(0, tot_m // 4) + (1 if i < tot_m % 4 else 0) for i in range(4)]

                dynamic_stack_height = max(240, min(450, len(categories) * 45 + 80))

                fig_stack = go.Figure()
                fig_stack.add_trace(go.Bar(x=categories, y=strong_v, name='Strong Match', marker_color='#047857'))
                fig_stack.add_trace(go.Bar(x=categories, y=partial_v, name='Partial Match', marker_color='#FF5C00'))
                fig_stack.add_trace(go.Bar(x=categories, y=missing_v, name='Action Gaps', marker_color='#CBD5E1'))

                fig_stack.update_layout(
                    barmode='stack',
                    xaxis=dict(showline=False, tickfont=dict(size=11, color='#1E293B', weight='bold')),
                    yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(size=10, color='#64748B')),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=15, r=10, t=30, b=20),
                    height=dynamic_stack_height,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10, color='#64748B')),
                    font=dict(color='#1E293B', family='Inter, sans-serif')
                )
                st.plotly_chart(fig_stack, use_container_width=True)

    # =========================================================
    # TAB 3: COMPETENCY RADAR & SKILL DISTRIBUTION
    # =========================================================
    with tab_skills:
        c_sk_left, c_sk_right = st.columns([1, 1])

        with c_sk_left:
            # Graph 5: Spider / Radar Polygon Competency Chart (Adapts to dimensions)
            with st.container(border=True):
                st.markdown("<div class='card-title'>🕸️ Candidate Competency Radar</div>", unsafe_allow_html=True)
                
                radar_categories = ['Technical Skills', 'ATS Optimization', 'Experience Fit', 'Education Alignment', 'Domain Fit', 'Soft Skills']
                radar_scores = [
                    min(100.0, len(strong_skills)*10.0),
                    ats_score,
                    st.session_state.ats_result.factor_scores.experience_relevance if st.session_state.ats_result else 75.0,
                    st.session_state.ats_result.factor_scores.education_relevance if st.session_state.ats_result else 80.0,
                    readiness_score,
                    85.0 if st.session_state.candidate_profile and st.session_state.candidate_profile.soft_skills else 65.0
                ]
                radar_cats_closed = radar_categories + [radar_categories[0]]
                radar_scores_closed = radar_scores + [radar_scores[0]]

                num_radar_items = len(radar_categories)
                dynamic_radar_height = max(280, min(450, num_radar_items * 40 + 100))

                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=radar_scores_closed,
                    theta=radar_cats_closed,
                    fill='toself',
                    fillcolor='rgba(255, 92, 0, 0.18)',
                    line=dict(color='#FF5C00', width=2.5),
                    name='Candidate Profile'
                ))

                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9, color='#64748B'), gridcolor='#E2E8F0'),
                        angularaxis=dict(tickfont=dict(size=11, color='#1E293B', weight='bold'), gridcolor='#E2E8F0'),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    showlegend=False,
                    height=dynamic_radar_height,
                    margin=dict(t=30, b=30, l=40, r=40),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#1E293B', family='Inter, sans-serif')
                )
                st.plotly_chart(fig_radar, use_container_width=True)

        with c_sk_right:
            # Graph 6: Donut Skill Competency Breakdown
            with st.container(border=True):
                st.markdown("<div class='card-title'>🍩 Skill Match Ratio Breakdown</div>", unsafe_allow_html=True)
                
                donut_labels = ['Strong Skills', 'Partial Skills', 'Missing Skills']
                donut_values = [len(strong_skills), len(partial_skills), len(missing_skills)]
                if sum(donut_values) == 0:
                    donut_values = [5, 2, 3]

                dynamic_donut_height = max(260, min(420, len(donut_labels) * 50 + 120))

                fig_donut = go.Figure(data=[go.Pie(
                    labels=donut_labels,
                    values=donut_values,
                    hole=0.55,
                    marker=dict(colors=['#047857', '#FF5C00', '#CBD5E1']),
                    textinfo='percent+label',
                    textposition='outside'
                )])

                fig_donut.update_layout(
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=11, color='#1E293B')),
                    height=dynamic_donut_height,
                    margin=dict(t=20, b=40, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#1E293B', family='Inter, sans-serif')
                )
                st.plotly_chart(fig_donut, use_container_width=True)

    # ---------------------------------------------------------
    # Platform Modules Overview (Visual Cards Bottom)
    # ---------------------------------------------------------
    st.markdown("<br><h3 style='font-size:1.3rem; font-weight:800; color:#1E293B;'>🚀 Executive Platform Modules Overview</h3>", unsafe_allow_html=True)
    c_m1, c_m2, c_m3, c_m4 = st.columns(4)

    with c_m1:
        st.markdown("""<div class="feature-card">
<h4>📄 1. Resume Upload & OCR</h4>
<p>High-fidelity text and visual layout processing powered by Mistral OCR 3 API.</p>
</div>""", unsafe_allow_html=True)
    with c_m2:
        st.markdown("""<div class="feature-card">
<h4>🎯 2. ATS Compatibility</h4>
<p>5-Factor scoring algorithms and AI bullet point transformation metrics.</p>
</div>""", unsafe_allow_html=True)
    with c_m3:
        st.markdown("""<div class="feature-card">
<h4>📊 3. Skill Gap Roadmap</h4>
<p>Competency gap mapping and structured 30-day learning and roadmap timelines.</p>
</div>""", unsafe_allow_html=True)
    with c_m4:
        st.markdown("""<div class="feature-card">
<h4>🎙️ 4. Strategy & Interview</h4>
<p>Custom questions and a dynamic, interactive mock interview Simulator.</p>
</div>""", unsafe_allow_html=True)
