"""
Project Recommendation Engine for Career मार्ग.
Suggests targeted, portfolio-ready project ideas to directly bridge candidate skill gaps.
"""

from typing import List, Dict, Any
from models.schemas import CandidateProfile, ProjectRecommendation
from services.llm_service import LLMService


class RecommendationService:
    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()

    def generate_project_recommendations(
        self,
        candidate_profile: CandidateProfile,
        target_role: str,
        missing_skills: List[str]
    ) -> List[ProjectRecommendation]:
        """
        Generates targeted project recommendations covering missing skill gaps.
        """
        gaps = missing_skills or ["Docker", "MLOps", "FastAPI", "Kubernetes"]
        role = target_role or "Machine Learning Engineer"

        projects = []

        # Project 1: Microservice & Containerization Focus
        gap1 = gaps[:2] if len(gaps) >= 2 else ["Docker", "REST API"]
        projects.append(ProjectRecommendation(
            title="Containerized Machine Learning Model Serving API",
            problem_statement=f"Build and package a production-grade machine learning model inference endpoint into Docker containers with automated health checks for {role} applications.",
            skills_developed=gap1 + ["Python", "FastAPI"],
            tech_stack=["FastAPI", "Docker", "Python", "PyTest", "GitHub Actions"],
            difficulty="Intermediate",
            employability_reason="Demonstrates ability to transition ML models from Jupyter Notebooks into scalable production microservices.",
            gap_skills_covered=gap1
        ))

        # Project 2: MLOps / Model Tracking Focus
        gap2 = gaps[2:4] if len(gaps) >= 4 else ["MLOps", "CI/CD"]
        projects.append(ProjectRecommendation(
            title="Automated MLOps Pipeline with Model Monitoring",
            problem_statement="Develop an automated retraining pipeline that monitors model drift, logs metrics to MLflow, and executes CI/CD unit tests upon dataset updates.",
            skills_developed=gap2 + ["Python", "MLflow"],
            tech_stack=["MLflow", "Docker", "Python", "Scikit-Learn", "PostgreSQL"],
            difficulty="Advanced",
            employability_reason="Proves enterprise readiness by mastering modern model lifecycle management and continuous deployment.",
            gap_skills_covered=gap2
        ))

        # Project 3: Full Stack AI Interactive Application
        gap3 = [gaps[0]] if gaps else ["Streamlit"]
        projects.append(ProjectRecommendation(
            title="Interactive Multimodal Document Analytics Dashboard",
            problem_statement="Engineered a web-based dashboard allowing users to upload multi-page PDF/Image documents, extract structured schemas, and perform real-time Q&A.",
            skills_developed=gap3 + ["Streamlit", "Python", "NLP"],
            tech_stack=["Streamlit", "Python", "Mistral API", "Plotly", "SQLite"],
            difficulty="Beginner-Intermediate",
            employability_reason="Provides an immediate, visually compelling portfolio project to demonstrate during live technical interviews.",
            gap_skills_covered=gap3
        ))

        return projects
