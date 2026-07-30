"""
Career Role Recommendation & Industry Readiness Service for Career मार्ग.
Recommends suitable career tracks based on candidate skills and calculates transparent Industry Readiness scores.
"""

from typing import List, Dict, Any
from models.schemas import CandidateProfile, CareerRecommendation, IndustryReadinessResult
from utils.scoring import calculate_industry_readiness
from services.llm_service import LLMService


BENCHMARK_ROLES = [
    {
        "role_name": "Machine Learning Engineer",
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Docker", "REST API", "Git"],
        "next_steps": ["Master MLOps container deployment with Docker & Kubernetes", "Build an end-to-end model serving API"]
    },
    {
        "role_name": "Data Scientist",
        "required_skills": ["Python", "Machine Learning", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Tableau", "Statistics"],
        "next_steps": ["Enhance statistical hypothesis testing portfolio projects", "Master advanced SQL database queries"]
    },
    {
        "role_name": "Full Stack AI Developer",
        "required_skills": ["Python", "JavaScript", "React", "Node.js", "FastAPI", "REST API", "SQL", "Docker"],
        "next_steps": ["Integrate LLM API calls with React interactive frontend", "Deploy application on AWS / GCP"]
    },
    {
        "role_name": "Data Analyst",
        "required_skills": ["SQL", "Python", "Pandas", "Excel", "Tableau", "Power BI", "Communication"],
        "next_steps": ["Create an interactive Power BI dashboard", "Practice complex SQL window functions"]
    },
    {
        "role_name": "Backend Software Engineer",
        "required_skills": ["Python", "Java", "REST API", "SQL", "PostgreSQL", "Docker", "Microservices", "Git"],
        "next_steps": ["Design microservices architecture with Redis caching", "Implement CI/CD automated test pipelines"]
    }
]


class CareerService:
    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    def recommend_career_roles(self, candidate_profile: CandidateProfile) -> List[CareerRecommendation]:
        """
        Calculates skill match percentage against industry benchmark roles.
        """
        candidate_skills = set(s.strip().lower() for s in candidate_profile.technical_skills + candidate_profile.soft_skills)
        recommendations = []

        for role_def in BENCHMARK_ROLES:
            req_skills = set(s.lower() for s in role_def["required_skills"])
            matching = candidate_skills.intersection(req_skills)
            missing = req_skills - candidate_skills

            match_pct = (len(matching) / len(req_skills)) * 100.0 if req_skills else 50.0
            
            # Boost if candidate has relevant projects
            proj_text = " ".join([p.title + " " + p.description for p in candidate_profile.projects]).lower()
            if role_def["role_name"].lower() in proj_text or any(m in proj_text for m in matching):
                match_pct += 10.0

            match_pct = min(98.0, max(45.0, match_pct))

            matching_display = [s.capitalize() for s in role_def["required_skills"] if s.lower() in matching]
            missing_display = [s.capitalize() for s in role_def["required_skills"] if s.lower() in missing]

            recommendations.append(CareerRecommendation(
                role_name=role_def["role_name"],
                match_percentage=round(match_pct, 1),
                matching_skills=matching_display or ["Foundational Programming"],
                missing_skills=missing_display,
                recommended_next_steps=role_def["next_steps"]
            ))

        # Sort descending by match percentage
        recommendations.sort(key=lambda r: r.match_percentage, reverse=True)
        return recommendations

    def evaluate_industry_readiness(
        self,
        candidate_profile: CandidateProfile,
        ats_score: float = 75.0,
        skill_gap_percentage: float = 25.0,
        mock_interview_score: float = 70.0
    ) -> IndustryReadinessResult:
        """
        Generates Industry Readiness score and transparent category breakdown.
        """
        tech_count = len(candidate_profile.technical_skills)
        proj_count = len(candidate_profile.projects)
        work_years = len(candidate_profile.work_experience) * 1.5

        return calculate_industry_readiness(
            tech_skills_count=tech_count,
            projects_count=proj_count,
            work_exp_years=work_years,
            ats_score=ats_score,
            skill_gap_percentage=skill_gap_percentage,
            mock_interview_avg_score=mock_interview_score
        )
