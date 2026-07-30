"""
Scoring and Evaluation Algorithms for Career मार्ग.
Implements transparent, factor-weighted scoring for ATS compatibility and Industry Readiness.
"""

from typing import Dict, List, Tuple, Any
from models.schemas import FactorScores, ATSResult, IndustryReadinessResult


def calculate_ats_score(
    candidate_skills: List[str],
    target_required_skills: List[str],
    resume_text: str,
    job_description_text: str,
    years_experience: float,
    required_years: float,
    has_degree_match: bool,
    document_layout_quality: float
) -> FactorScores:
    """
    Computes ATS Factor Scores with transparent weights:
    - Required skill match: 40%
    - Keyword match: 25%
    - Experience relevance: 15%
    - Education relevance: 10%
    - Structure quality: 10%
    """
    # 1. Required Skill Match (40%)
    if target_required_skills:
        matched = set(s.lower() for s in candidate_skills).intersection(
            set(s.lower() for s in target_required_skills)
        )
        skill_score = (len(matched) / len(target_required_skills)) * 100.0
    else:
        skill_score = 75.0  # Default baseline if no explicit target skills specified

    skill_score = min(100.0, max(0.0, skill_score))

    # 2. Keyword Match (25%)
    jd_words = set(w.lower() for w in job_description_text.split() if len(w) > 3) if job_description_text else set()
    resume_words = set(w.lower() for w in resume_text.split() if len(w) > 3) if resume_text else set()
    
    if jd_words:
        keyword_overlap = len(jd_words.intersection(resume_words))
        keyword_score = (keyword_overlap / len(jd_words)) * 100.0 * 2.5  # scaling factor
        keyword_score = min(100.0, max(10.0, keyword_score))
    else:
        keyword_score = 70.0

    # 3. Experience Relevance (15%)
    if required_years > 0:
        exp_score = (years_experience / required_years) * 100.0
        exp_score = min(100.0, max(20.0, exp_score))
    else:
        exp_score = 85.0

    # 4. Education Relevance (10%)
    edu_score = 95.0 if has_degree_match else 60.0

    # 5. Structure Quality (10%)
    structure_score = min(100.0, max(0.0, document_layout_quality))

    return FactorScores(
        required_skill_match=round(skill_score, 1),
        keyword_match=round(keyword_score, 1),
        experience_relevance=round(exp_score, 1),
        education_relevance=round(edu_score, 1),
        structure_quality=round(structure_score, 1)
    )


def compute_weighted_ats_overall(factors: FactorScores) -> float:
    """
    Computes overall ATS score from weighted sub-factors.
    Weights: 40% skills, 25% keywords, 15% experience, 10% education, 10% structure.
    """
    overall = (
        factors.required_skill_match * 0.40 +
        factors.keyword_match * 0.25 +
        factors.experience_relevance * 0.15 +
        factors.education_relevance * 0.10 +
        factors.structure_quality * 0.10
    )
    return round(overall, 1)


def calculate_industry_readiness(
    tech_skills_count: int,
    projects_count: int,
    work_exp_years: float,
    ats_score: float,
    skill_gap_percentage: float,
    mock_interview_avg_score: float
) -> IndustryReadinessResult:
    """
    Calculates transparent Industry Readiness score (0-100) across 6 weighted categories:
    - Technical Skills (25%)
    - Project Quality (20%)
    - Work Experience (20%)
    - Resume Quality / ATS Fit (15%)
    - Target Role Alignment (10%)
    - Interview Readiness (10%)
    """
    # Technical skills score (benchmark: 8+ relevant skills)
    tech_score = min(100.0, (tech_skills_count / 8.0) * 100.0)
    
    # Project quality score (benchmark: 3+ projects)
    project_score = min(100.0, (projects_count / 3.0) * 100.0)
    
    # Work experience score (benchmark: 2+ years / internships)
    exp_score = min(100.0, max(30.0, (work_exp_years / 2.0) * 100.0))
    
    # Resume quality / ATS score
    resume_score = max(0.0, ats_score)
    
    # Target role alignment (100 - gap percentage)
    alignment_score = max(20.0, 100.0 - skill_gap_percentage)
    
    # Interview readiness score
    interview_score = max(40.0, mock_interview_avg_score)
    
    category_scores = {
        "Technical Skills": round(tech_score, 1),
        "Project Quality": round(project_score, 1),
        "Work Experience": round(exp_score, 1),
        "Resume Quality": round(resume_score, 1),
        "Target Role Alignment": round(alignment_score, 1),
        "Interview Readiness": round(interview_score, 1)
    }
    
    overall = (
        tech_score * 0.25 +
        project_score * 0.20 +
        exp_score * 0.20 +
        resume_score * 0.15 +
        alignment_score * 0.10 +
        interview_score * 0.10
    )
    
    strengths = []
    weaknesses = []
    action_plan = []
    
    if tech_score >= 75:
        strengths.append("Strong technical skill foundational coverage.")
    else:
        weaknesses.append("Technical skill inventory can be expanded.")
        action_plan.append("Acquire high-demand technical skills identified in missing skill gaps.")
        
    if project_score >= 70:
        strengths.append("Solid portfolio of practical projects.")
    else:
        weaknesses.append("Limited quantity or depth of portfolio projects.")
        action_plan.append("Build and showcase at least 2 end-to-end industry-aligned projects.")
        
    if resume_score >= 75:
        strengths.append("High ATS compliance and resume formatting quality.")
    else:
        weaknesses.append("Resume formatting or keyword alignment needs improvement.")
        action_plan.append("Incorporate quantitative metrics and targeted keywords into work experience bullets.")

    return IndustryReadinessResult(
        overall_score=round(overall, 1),
        category_scores=category_scores,
        strengths=strengths,
        weaknesses=weaknesses,
        actionable_improvement_plan=action_plan
    )
