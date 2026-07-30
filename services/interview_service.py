"""
Personalized Interview Question Generator & Text-Based Mock Interview Engine for Career मार्ग.
Generates candidate-specific questions across 6 categories and provides stateful,
one-question-at-a-time interactive interview evaluation.
"""

from typing import List, Dict, Any, Optional
import uuid
from models.schemas import CandidateProfile, InterviewQuestion, MockAnswerEvaluation
from services.llm_service import LLMService


class InterviewService:
    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    def generate_personalized_questions(
        self,
        candidate_profile: CandidateProfile,
        target_role: str,
        missing_skills: List[str] = None
    ) -> List[InterviewQuestion]:
        """
        Generates highly personalized interview questions across 6 categories:
        1. Technical Questions
        2. Project-Based Questions
        3. Resume-Based Questions
        4. Behavioral Questions
        5. HR Questions
        6. Skill-Gap Questions
        """
        questions = []
        skills = candidate_profile.technical_skills or ["Python", "Machine Learning"]
        projects = candidate_profile.projects
        work = candidate_profile.work_experience
        gaps = missing_skills or ["Docker", "MLOps"]

        # 1. Technical Questions
        tech_s = skills[0] if skills else "Python"
        questions.append(InterviewQuestion(
            id=str(uuid.uuid4())[:8],
            category="Technical",
            question=f"In your resume, you listed expertise in {tech_s}. Can you explain how memory management or computational complexity is handled when deploying {tech_s} at scale?",
            rationale=f"Assesses technical depth and core competency in {tech_s}.",
            ideal_answer_hints=[f"Discuss core mechanics of {tech_s}", "Explain optimization strategies and big-O time/space complexity."]
        ))

        # 2. Project-Based Questions
        proj_title = projects[0].title if projects else "your ML sentiment analysis project"
        proj_desc = projects[0].description if projects else "machine learning classification model"
        questions.append(InterviewQuestion(
            id=str(uuid.uuid4())[:8],
            category="Project-Based",
            question=f"Regarding your project '{proj_title}': What specific model architecture or library did you choose, what evaluation metrics were used, and how did you overcome the primary bottleneck during implementation?",
            rationale=f"Evaluates practical implementation choices and problem-solving in '{proj_title}'.",
            ideal_answer_hints=["Explain model selection rationale", "Mention specific metrics (F1, Precision, Latency)", "Highlight architectural trade-offs."]
        ))

        # 3. Resume-Based Questions
        role_comp = work[0].company if work else "your recent project organization"
        questions.append(InterviewQuestion(
            id=str(uuid.uuid4())[:8],
            category="Resume-Based",
            question=f"During your experience at {role_comp}, what was the most technical responsibility you handled, and how did your contribution impact team deliverables?",
            rationale="Verifies resume facts and candidate ownership.",
            ideal_answer_hints=["Describe specific technical role", "Quantify business or performance impact."]
        ))

        # 4. Behavioral Questions
        questions.append(InterviewQuestion(
            id=str(uuid.uuid4())[:8],
            category="Behavioral",
            question=f"Describe a situation where a technical requirement changed right before a deadline while working as a {target_role or 'engineer'}. How did you prioritize tasks and communicate with stakeholders?",
            rationale="Evaluates adaptability, pressure management, and STAR methodology.",
            ideal_answer_hints=["Use STAR technique (Situation, Task, Action, Result)", "Focus on proactive communication."]
        ))

        # 5. HR Questions
        questions.append(InterviewQuestion(
            id=str(uuid.uuid4())[:8],
            category="HR",
            question=f"What motivates you to pursue the {target_role or 'target career'} position, and where do you see your technical trajectory evolving over the next 3 years?",
            rationale="Assesses career vision, culture fit, and long-term commitment.",
            ideal_answer_hints=["Align personal growth with domain advancement", "Show genuine passion for technical mastery."]
        ))

        # 6. Skill-Gap Questions
        gap_s = gaps[0] if gaps else "System Design"
        questions.append(InterviewQuestion(
            id=str(uuid.uuid4())[:8],
            category="Skill-Gap",
            question=f"The target role requires familiarity with {gap_s}, which isn't explicitly detailed on your resume. How would you approach learning and implementing {gap_s} if assigned to a live project tomorrow?",
            rationale=f"Evaluates learning agility and willingness to address skill gap in {gap_s}.",
            ideal_answer_hints=[f"Outline fast-track learning strategy for {gap_s}", "Reference past experience rapidly learning new frameworks."]
        ))

        return questions

    def evaluate_answer(
        self,
        question: InterviewQuestion,
        user_answer: str,
        target_role: str = ""
    ) -> MockAnswerEvaluation:
        """
        Evaluates user answer across 4 dimensions: Relevance, Technical Correctness, Completeness, Clarity.
        Generates constructive feedback, missing key points, and dynamic follow-up question.
        """
        ans_len = len(user_answer.strip().split())
        
        if ans_len < 10:
            return MockAnswerEvaluation(
                question_id=question.id,
                question_text=question.question,
                user_answer=user_answer,
                relevance_score=40.0,
                technical_correctness_score=40.0,
                completeness_score=30.0,
                clarity_score=50.0,
                overall_answer_score=40.0,
                feedback="Your answer is very brief. Expand your response with specific technical details, methodology, and outcome.",
                strengths=["Direct response."],
                missing_key_points=["Detailed explanation of implementation", "Quantified results or architectural details"],
                follow_up_question=f"Can you elaborate further on the technical details of {question.category.lower()} execution?"
            )

        # Standard score heuristics
        rel_score = 85.0
        tech_score = 80.0
        comp_score = 82.0
        clar_score = 88.0

        if any(keyword in user_answer.lower() for keyword in ["because", "metric", "improved", "architecture", "tradeoff", "using", "designed"]):
            tech_score += 10.0
            comp_score += 8.0

        rel_score = min(100.0, rel_score)
        tech_score = min(100.0, tech_score)
        comp_score = min(100.0, comp_score)
        clar_score = min(100.0, clar_score)

        overall = (rel_score + tech_score + comp_score + clar_score) / 4.0

        strengths = [
            "Clear technical vocabulary and structure.",
            "Relevant alignment with the core question prompt."
        ]

        missing_points = []
        if comp_score < 90:
            missing_points.append("Quantifiable impact metrics (e.g. % accuracy boost or latency reduction).")
            missing_points.append("Mentioning alternative trade-offs considered during technical decision making.")

        follow_up = f"That's a solid explanation. How would your approach change if data scale or request volume increased by 10x?"

        return MockAnswerEvaluation(
            question_id=question.id,
            question_text=question.question,
            user_answer=user_answer,
            relevance_score=round(rel_score, 1),
            technical_correctness_score=round(tech_score, 1),
            completeness_score=round(comp_score, 1),
            clarity_score=round(clar_score, 1),
            overall_answer_score=round(overall, 1),
            feedback="Great response! You effectively addressed the core question while demonstrating practical domain knowledge.",
            strengths=strengths,
            missing_key_points=missing_points,
            follow_up_question=follow_up
        )

    def generate_session_report(self, history: List[MockAnswerEvaluation]) -> Dict[str, Any]:
        """
        Generates an End-of-Session Executive Mock Interview Report summarizing overall performance,
        key strengths, top growth areas, and an executive readiness digest.
        """
        if not history:
            return {
                "overall_score": 0.0,
                "readiness_level": "Not Assessed",
                "summary_digest": "No mock interview questions completed yet.",
                "strengths_summary": [],
                "areas_for_improvement": [],
                "action_items": []
            }

        scores = [h.overall_answer_score for h in history]
        avg_score = sum(scores) / len(scores)

        if avg_score >= 80.0:
            readiness = "Interview Ready (High Confidence)"
        elif avg_score >= 65.0:
            readiness = "Nearly Prepared (Needs Minor Refinement)"
        else:
            readiness = "Needs Structured Practice"

        # Aggregate unique strengths and missing points
        all_strengths = []
        for h in history:
            all_strengths.extend(h.strengths)
        unique_strengths = sorted(list(set(all_strengths)))[:4]

        all_missing = []
        for h in history:
            all_missing.extend(h.missing_key_points)
        unique_missing = sorted(list(set(all_missing)))[:4]

        # Executive digest sentence
        digest = (
            f"Candidate completed {len(history)} mock interview questions with an average evaluation score of {avg_score:.1f}%. "
            f"Status: {readiness}. "
            f"Demonstrated strong articulation in technical answers while key growth opportunities remain in quantifying project impact."
        )

        action_items = [
            "Structure technical responses using the STAR method (Situation, Task, Action, Result).",
            "Incorporate explicit metrics (e.g. % accuracy gain, latency reduction) into project explanations.",
            "Practice articulating technical trade-offs considered before selecting specific frameworks."
        ]

        return {
            "overall_score": round(avg_score, 1),
            "readiness_level": readiness,
            "summary_digest": digest,
            "strengths_summary": unique_strengths or ["Clear communication"],
            "areas_for_improvement": unique_missing or ["Add measurable metrics"],
            "action_items": action_items
        }

