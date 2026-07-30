"""
Streamlit Page 5: Text-Based Interactive Mock Interview Engine
"""

import streamlit as st

from utils.helpers import init_session_state, apply_custom_style
from services.interview_service import InterviewService
from data.database import save_interview_turn

st.set_page_config(page_title="Text Mock Interview - Career मार्ग", page_icon="🎙️", layout="wide")
init_session_state(st.session_state)
apply_custom_style(active_page="mock_interview")

st.title("🎙️ Text-Based Interactive Mock Interview")
st.caption("One-question-at-a-time live practice session with immediate scoring, feedback, and dynamic follow-up questions")
st.divider()

if not st.session_state.candidate_profile:
    st.warning("⚠️ No resume loaded. Please upload your resume on **1_Resume_Analysis** first.")
    st.stop()

# Initialize Questions list if empty
if not st.session_state.interview_questions:
    int_service = InterviewService()
    st.session_state.interview_questions = int_service.generate_personalized_questions(
        candidate_profile=st.session_state.candidate_profile,
        target_role=st.session_state.target_job_role or "Machine Learning Engineer"
    )

questions = st.session_state.interview_questions
curr_idx = st.session_state.current_question_index

if curr_idx < len(questions):
    current_q = questions[curr_idx]
    
    st.markdown(f"### **Question {curr_idx + 1} of {len(questions)}** `[{current_q.category}]`")
    st.info(f"❓ **{current_q.question}**")

    # Text Input for Candidate Answer
    user_answer = st.text_area("Your Response (Text-Based Only):", height=150, key=f"q_ans_{curr_idx}")

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        submit_btn = st.button("Submit Answer 🚀", type="primary")

    if submit_btn and user_answer.strip():
        with st.spinner("Evaluating response quality, technical depth, and completeness..."):
            int_svc = InterviewService()
            eval_res = int_svc.evaluate_answer(current_q, user_answer, st.session_state.target_job_role)
            
            st.session_state.mock_interview_history.append(eval_res)

            # Persist turn
            try:
                save_interview_turn(
                    session_id="mock_session_1",
                    question=current_q.question,
                    user_answer=user_answer,
                    score=eval_res.overall_answer_score,
                    eval_dict=eval_res.dict()
                )
            except Exception:
                pass

            st.success("✓ Response evaluated!")

# Render Evaluation History & Progress
if st.session_state.mock_interview_history:
    st.divider()
    st.subheader("📋 Executive End-of-Session Interview Report")

    int_svc = InterviewService()
    session_report = int_svc.generate_session_report(st.session_state.mock_interview_history)

    r_col1, r_col2 = st.columns([1, 1.3])
    with r_col1:
        st.metric("Overall Session Readiness", session_report["readiness_level"], delta=f"{session_report['overall_score']:.1f}% Avg Score")
        st.info(f"💡 **Executive Digest:** {session_report['summary_digest']}")

    with r_col2:
        st.markdown("#### **Actionable Recommendation Items**")
        for item in session_report["action_items"]:
            st.success(f"• {item}")

    st.divider()
    st.subheader("📊 Turn-by-Turn Question History")

    for idx, record in enumerate(st.session_state.mock_interview_history, 1):
        with st.expander(f"Question #{idx} Evaluation: Score {record.overall_answer_score:.1f}%"):
            st.markdown(f"**Question:** {record.question_text}")
            st.markdown(f"**Your Answer:** {record.user_answer}")
            
            s1, s2, s3, s4 = st.columns(4)
            s1.metric("Relevance", f"{record.relevance_score}%")
            s2.metric("Technical Depth", f"{record.technical_correctness_score}%")
            s3.metric("Completeness", f"{record.completeness_score}%")
            s4.metric("Clarity", f"{record.clarity_score}%")

            st.markdown(f"**Feedback:** {record.feedback}")
            
            if record.strengths:
                st.markdown("**Strengths:**")
                for str_item in record.strengths:
                    st.success(f"• {str_item}")

            if record.missing_key_points:
                st.markdown("**Points to Improve:**")
                for miss in record.missing_key_points:
                    st.warning(f"• {miss}")

            if record.follow_up_question:
                st.markdown(f"💬 **Dynamic Follow-Up Question:** *{record.follow_up_question}*")

    # Next Question Button
    if curr_idx < len(questions) - 1:
        if st.button("Proceed to Next Question ➡️"):
            st.session_state.current_question_index += 1
            st.rerun()
    else:
        st.divider()
        st.success("🎉 Mock Interview Session Complete!")

